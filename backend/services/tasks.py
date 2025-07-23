from celery import shared_task
from models.user import User
from models.reservation import Reservation
from datetime import datetime, timedelta
from utils.notifications import send_reminder, send_monthly_report, send_csv
from sqlalchemy import func
from datetime import datetime, timedelta
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)



@shared_task(ignore_result=True)
def send_daily_reminders():
    from app import create_app
    app = create_app()
    with app.app_context():
        tomorrow = datetime.utcnow() + timedelta(days=1)
        users = User.query.join(Reservation).filter(
            Reservation.reserved_at.between(
                tomorrow.replace(hour=0, minute=0, second=0),
                tomorrow.replace(hour=23, minute=59, second=59)
            )
        ).all()
        
        for user in users:
            send_reminder(user)

@shared_task(ignore_result=True)
def send_monthly_reports():
    from app import create_app
    app = create_app()
    with app.app_context():
        first_day = datetime.utcnow().replace(day=1) - timedelta(days=1)
        first_day = first_day.replace(day=1)
        last_day = datetime.utcnow().replace(day=1) - timedelta(days=1)
        
        users = User.query.all()
        for user in users:
            send_monthly_report(user)





@shared_task(ignore_result=True)
def generate_csv_export(user_id=None, admin_id=None):
    from app import create_app
    app = create_app()
    with app.app_context():
        from io import StringIO
        import csv

        output = StringIO()
        writer = csv.writer(output)
        success = False  # Track email status

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
                print(f"✅ Email sent successfully to {user.email}")
            else:
                print(f"❌ Failed to send email to {user.email}")

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
                print(f"✅ Admin report sent to {admin.email}")
            else:
                print(f"❌ Failed to send admin report to {admin.email}")
