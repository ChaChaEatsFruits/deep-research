from dotenv import load_dotenv
import requests
import os
import smtplib
from email.message import EmailMessage
load_dotenv(override=True)


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

USE_EMAIL = bool(EMAIL_ADDRESS and RESEND_API_KEY)
print("Resend is set up" if USE_EMAIL else "Resend not set up; falling back to push")

def send_email(subject, text_body, html_body):
    r = requests.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
        json={
            "from": "ComplAI Sales <onboarding@resend.dev>",
            "to": [EMAIL_ADDRESS],
            "subject": subject,
            "text": text_body,
            "html": html_body,
        },
    )
    r.raise_for_status()  # so failures show up instead of being silent
    return r.json()


pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

def push(message):
    print(f"Push: {message}")
    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    requests.post(pushover_url, data=payload)

