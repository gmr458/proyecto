from email.message import EmailMessage
import os
import smtplib
import aiosmtplib
import ssl
import sys

EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
if EMAIL_SENDER is None or EMAIL_SENDER == "":
    print("Environment variable EMAIL_SENDER does not exists")
    sys.exit()

PASSWORD_SENDER = os.environ.get("PASSWORD_SENDER")
if PASSWORD_SENDER is None or PASSWORD_SENDER == "":
    print("Environment variable PASSWORD_SENDER does not exists")
    sys.exit()

SMTP_HOST = os.environ.get("SMTP_HOST")
if SMTP_HOST is None or SMTP_HOST == "":
    print("Environment variable SMTP_HOST does not exists")
    sys.exit()


async def send_email_async(email_receiver: str, subject: str, body: str):
    email_message = EmailMessage()
    email_message["From"] = EMAIL_SENDER
    email_message["To"] = email_receiver
    email_message["Subject"] = subject
    email_message.set_content(body)

    context = ssl.create_default_context()

    async with aiosmtplib.SMTP(
        hostname=SMTP_HOST,
        port=587,
        tls_context=context,
    ) as smtp:
        await smtp.login(EMAIL_SENDER, PASSWORD_SENDER)
        await smtp.sendmail(EMAIL_SENDER, email_receiver, email_message.as_string())


def send_email(email_receiver: str, subject: str, body: str):
    email_message = EmailMessage()
    email_message["From"] = EMAIL_SENDER
    email_message["To"] = email_receiver
    email_message["Subject"] = subject
    email_message.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMTP_HOST, 465, context=context) as smtp:
        smtp.login(EMAIL_SENDER, PASSWORD_SENDER)
        smtp.sendmail(EMAIL_SENDER, email_receiver, email_message.as_string())
