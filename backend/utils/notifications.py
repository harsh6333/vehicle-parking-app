import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from jinja2 import Environment, FileSystemLoader
import os
import pdfkit
from datetime import datetime, timedelta
from sqlalchemy import func
from config import Config

def send_email(to, subject, body, html=None, attachment=None, attachment_name="report.csv"):
    msg = MIMEMultipart()
    msg['From'] = Config.MAIL_DEFAULT_SENDER
    msg['To'] = to
    msg['Subject'] = subject

    if html:
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
        print(f"[✔] Email sent to {to} with subject: {subject}")
        return True
    except Exception as e:
        print(f"[✖] Error sending email to {to}: {e}")
        return False


def send_reminder(user):
    from models.reservation import Reservation
    tomorrow = datetime.utcnow().date() + timedelta(days=1)
    reservations = Reservation.query.filter_by(user_id=user.id).filter(
        func.date(Reservation.reserved_at) == tomorrow
    ).all()

    if not reservations:
        print(f"[ℹ] No reservations for {user.email} tomorrow.")
        return False

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('reminder_email.html')
    html = template.render(user=user, reservations=reservations)

    subject = f"Reminder: You have {len(reservations)} parking reservation(s) tomorrow"
    return send_email(user.email, subject, "", html)


def send_monthly_report(user):
    from models.reservation import Reservation

    first_day = datetime.utcnow().replace(day=1) - timedelta(days=1)
    first_day = first_day.replace(day=1)
    last_day = datetime.utcnow().replace(day=1) - timedelta(days=1)

    reservations = Reservation.query.filter_by(user_id=user.id).filter(
        Reservation.reserved_at.between(first_day, last_day)
    ).all()

    total_hours = sum(
        (r.reserved_till - r.reserved_at).total_seconds() / 3600
        for r in reservations
        if r.reserved_at and r.reserved_till
    )
    total_cost = sum(r.parking_cost for r in reservations)

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('monthly_report.html')
    html = template.render(
        user=user,
        reservations=reservations,
        total_hours=total_hours,
        total_cost=total_cost,
        month=first_day.strftime("%B %Y")
    )

    pdf_file = f"monthly_report_{user.id}.pdf"
    try:
        pdfkit.from_string(html, pdf_file)
        with open(pdf_file, 'rb') as f:
            attachment = f.read()
        result = send_email(user.email, f"Your Monthly Parking Report - {first_day.strftime('%B %Y')}", "", html, attachment, attachment_name=pdf_file)
        return result
    except Exception as e:
        print(f"[✖] Failed to generate/send PDF report: {e}")
        return False
    finally:
        if os.path.exists(pdf_file):
            os.remove(pdf_file)


def send_csv(to, subject, csv_data):
    return send_email(to, subject, "Please find attached your CSV report.", attachment=csv_data, attachment_name="report.csv")
