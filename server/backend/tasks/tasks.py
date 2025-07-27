import pytz
from backend.models.user import User
from backend.models.reservation import Reservation
from datetime import datetime, timedelta
from backend.utils.notifications import send_gentle_reminder_to_inactive_users, send_reminder, send_admin_monthly_report,send_user_monthly_report, send_csv
from sqlalchemy import func
from datetime import datetime, timedelta
from dotenv import load_dotenv

from backend.utils.timehelper import get_previous_month_bounds_as_naive_utc, get_tomorrow_ist_bounds_as_utc
load_dotenv()
import logging
logger = logging.getLogger(__name__)
from backend import create_app
app = create_app()
from celery import current_app as celery

@celery.task(name="backend.tasks.tasks.generate_csv_export")
def generate_csv_export(user_id=None, admin_id=None):
    from io import StringIO
    import csv
    output = StringIO()
    writer = csv.writer(output)
    success = False

    if user_id:
        reservations = Reservation.query.filter_by(user_id=user_id).all()
        writer.writerow(['Reservation ID', 'Spot ID', 'Start Time', 'End Time', 'Duration', 'Cost'])
        for r in reservations:
            duration = (r.reserved_till - r.reserved_at).total_seconds()/3600 if r.reserved_till else 0
            writer.writerow([
                r.id, r.spot_id, r.reserved_at, r.reserved_till,
                f"{duration:.2f} hours", r.parking_cost
            ])
        user = User.query.get(user_id)
        success = send_csv(user.email, "Your Parking History", output.getvalue())
        if success:
            print(f"Email sent successfully to {user.email}")
        else:
            print(f"Failed to send email to {user.email}")

    elif admin_id:
        writer.writerow(['User ID', 'Username', 'Total Reservations', 'Total Hours', 'Total Spending'])
        users = User.query.all()
        for user in users:
            total_hours = 0
            total_cost = 0
            for r in user.reservations:
                if r.reserved_at and r.reserved_till:
                    duration = (r.reserved_till - r.reserved_at).total_seconds()/3600
                    total_hours += duration
                    total_cost += duration * r.spot.lot.price
            writer.writerow([
                user.id, user.username, len(user.reservations),
                f"{total_hours:.2f}", f"₹{total_cost:.2f}"
            ])
        admin = User.query.get(admin_id)
        success = send_csv(admin.email, "System-wide Parking Report", output.getvalue())
        if success:
            print(f"Admin report sent to {admin.email}")
        else:
            print(f"Failed to send admin report to {admin.email}")



@celery.task(name="backend.tasks.tasks.send_daily_reminders")
def send_daily_reminders():
    india = pytz.timezone("Asia/Kolkata")
    tomorrow_ist = datetime.now(india).date() + timedelta(days=1)
    start_ist = india.localize(datetime.combine(tomorrow_ist, datetime.min.time()))
    end_ist = india.localize(datetime.combine(tomorrow_ist, datetime.max.time()))
    start_utc, end_utc = get_tomorrow_ist_bounds_as_utc()

    print(f"Checking reminders for: {tomorrow_ist}")
    print(f"[IST] {start_ist} - {end_ist}")
    print(f"[UTC] {start_utc} - {end_utc}")

    # Users who HAVE reservations tomorrow
    users_with_reservations = User.query.join(Reservation).filter(
        Reservation.reserved_at.between(start_utc, end_utc)
    ).all()

    print(f"[👥] Found {len(users_with_reservations)} users with reservations.")

    for user in users_with_reservations:
        print(f"[📨] Sending reminder to: {user.email}")
        send_reminder(user)

    # Send gentle reminder to others
    send_gentle_reminder_to_inactive_users(start_utc, end_utc, users_with_reservations)





@celery.task(name="backend.tasks.tasks.send_monthly_reports")
def send_monthly_reports():
    first_day_this_month, last_day_this_month = get_previous_month_bounds_as_naive_utc()
    users = User.query.all()
    for user in users:
        if user.is_admin:
            send_admin_monthly_report(user, first_day=first_day_this_month, last_day=last_day_this_month)
        else:
            send_user_monthly_report(user, first_day=first_day_this_month, last_day=last_day_this_month)
