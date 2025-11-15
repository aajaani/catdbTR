import smtplib
from email.mime.text import MIMEText
import os


SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USERNAME)


def send_email(to: str, subject: str, body: str):
    msg = MIMEText(body, "plain", "utf-8")
    msg['Subject'] = subject
    msg['From'] = SMTP_FROM
    msg['To'] = to

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp_server:
       smtp_server.starttls()
       smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)
       smtp_server.sendmail(SMTP_FROM, [to], msg.as_string())
    print("Message sent!")

