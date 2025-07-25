import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from jinja2 import Environment, FileSystemLoader
import os
import pytz
import pdfkit
from datetime import datetime, timedelta
from sqlalchemy import func
from backend.config import Config
from dotenv import load_dotenv
load_dotenv()
from backend.models.reservation import Reservation
import logging
logger = logging.getLogger(__name__)


TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')
TEMPLATES_DIR = os.path.abspath(TEMPLATES_DIR)  
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def send_email(to, subject, body, html=None, attachment=None, attachment_name="report.csv"):
    msg = MIMEMultipart()
    msg['From'] = Config.MAIL_DEFAULT_SENDER
    msg['To'] = to
    msg['Subject'] = subject
    if html:
        print('yes')
        msg.attach(MIMEText(html, 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))

    if attachment:
        part = MIMEApplication(attachment, Name=attachment_name)
        part['Content-Disposition'] = f'attachment; filename="{attachment_name}"'
        msg.attach(part)

    try:
        server = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
        server.starttls()
        server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
        server.sendmail(Config.MAIL_DEFAULT_SENDER, to, msg.as_string())
        server.quit()
        print(f"Email sent to {to} with subject: {subject}")
        return True
    except Exception as e:
        print(f"Error sendingiii email to {to}: {e}")
        return False


def send_reminder(user):
    # Convert IST "tomorrow" to UTC range
    india = pytz.timezone("Asia/Kolkata")
    utc = pytz.utc

    tomorrow_ist = datetime.now(india).date() + timedelta(days=1)
    start_ist = india.localize(datetime.combine(tomorrow_ist, datetime.min.time()))
    end_ist = india.localize(datetime.combine(tomorrow_ist, datetime.max.time()))

    start_utc = start_ist.astimezone(utc)
    end_utc = end_ist.astimezone(utc)

    reservations = Reservation.query.filter_by(user_id=user.id).filter(
        Reservation.reserved_at.between(start_utc, end_utc)
    ).all()

    if not reservations:
        print(f"No reservations for {user.email} tomorrow (IST).")
        return False
    
    template = env.get_template('reminder_email.html')
    html = template.render(user=user, reservations=reservations)

    subject = f"Reminder: You have {len(reservations)} parking reservation(s) tomorrow"
    return send_email(user.email, subject, "", html)



def send_user_monthly_report(user, first_day, last_day):
    reservations = Reservation.query.filter_by(user_id=user.id).filter(
        Reservation.reserved_at.between(first_day, last_day)
    ).all()

    total_hours = sum(
        (r.reserved_till - r.reserved_at).total_seconds() / 3600
        for r in reservations if r.reserved_at and r.reserved_till
    )
    total_cost = sum(r.parking_cost for r in reservations if r.parking_cost)


    template = env.get_template('monthly_user_report.html')
    html = template.render(
        user=user,
        reservations=reservations,
        total_hours=total_hours,
        total_cost=total_cost,
        month=first_day.strftime("%B %Y")
    )

    pdf_file = f"user_monthly_report_{user.id}.pdf"
    try:
        pdfkit.from_string(html, pdf_file)
        with open(pdf_file, 'rb') as f:
            attachment = f.read()
        return send_email(
            user.email,
            f"Your Monthly Parking Report - {first_day.strftime('%B %Y')}",
            "",
            html,
            attachment,
            attachment_name=pdf_file
        )
    except Exception as e:
        print(f"Failed to send user report to {user.email}: {e}")
    finally:
        if os.path.exists(pdf_file):
            os.remove(pdf_file)


def send_admin_monthly_report(admin_user, first_day, last_day):
    reservations = Reservation.query.filter(
        Reservation.reserved_at.between(first_day, last_day)
    ).all()

    total_hours = sum(
        (r.reserved_till - r.reserved_at).total_seconds() / 3600
        for r in reservations if r.reserved_at and r.reserved_till
    )
    total_cost = sum(r.parking_cost for r in reservations if r.parking_cost)

    # Group by user and lot
    from collections import defaultdict
    reservations_by_user = defaultdict(list)
    reservations_by_lot = defaultdict(list)

    for r in reservations:
        reservations_by_user[r.user.username].append(r)
        reservations_by_lot[r.spot.lot.prime_location_name].append(r)

    template = env.get_template('monthly_admin_report.html')
    html = template.render(
        admin=admin_user,
        reservations=reservations,
        reservations_by_user=reservations_by_user,
        reservations_by_lot=reservations_by_lot,
        total_hours=total_hours,
        total_cost=total_cost,
        month=first_day.strftime("%B %Y")
    )

    pdf_file = f"admin_monthly_report_{admin_user.id}.pdf"
    try:
        pdfkit.from_string(html, pdf_file)
        with open(pdf_file, 'rb') as f:
            attachment = f.read()
        return send_email(
            admin_user.email,
            f"Admin Monthly Report - {first_day.strftime('%B %Y')}",
            "",
            html,
            attachment,
            attachment_name=pdf_file
        )
    except Exception as e:
        print(f"Failed to send admin report: {e}")
    finally:
        if os.path.exists(pdf_file):
            os.remove(pdf_file)





def send_csv(to, subject, csv_data):
    return send_email(to, subject, "Please find attached your CSV report.", attachment=csv_data, attachment_name="report.csv")
