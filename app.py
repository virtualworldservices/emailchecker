from flask import Flask, render_template, request, redirect, url_for
import csv
import imaplib
import email
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Function to send emails
def send_email(to_email, to_name, subject, body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'rana@Virtualworld.services'
    smtp_password = 'evsfbuvkcvpuuzru'

    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = to_email
    message['Subject'] = subject

    body = f"Dear {to_name},\n\n{body}"
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, message.as_string())

# Function to check for bounced emails
def check_bounced_emails(to_email):
    imap_server = 'imap.gmail.com'
    imap_username = 'rana@Virtualworld.services'
    imap_password = 'evsfbuvkcvpuuzru'

    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(imap_username, imap_password)
    mail.select("inbox")

    # Search for emails with UNSEEN flag, which indicates new/unread emails
    result, data = mail.search(None, 'UNSEEN')

    bounced_emails = []

    if result == 'OK':
        for num in data[0].split():
            # Fetch the email and check if it has a bounce status
            result, email_data = mail.fetch(num, '(RFC822)')
            if result == 'OK':
                msg = str(email_data[0][1])
                if to_email in msg:
                    bounced_emails.append(to_email)

    mail.close()
    mail.logout()

    return bounced_emails

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    to_email = request.form['email']
    to_name = request.form['name']
    subject = "Test Subject"
    body = "This is a test email."

    send_email(to_email, to_name, subject, body)
    time.sleep(15)

    bounced_emails = check_bounced_emails(to_email)
    if to_email in bounced_emails:
        result = f"Email to {to_email} bounced."
    else:
        result = f"Email to {to_email} delivered successfully."

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
