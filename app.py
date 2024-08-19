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
    subject = "Elevate Your Business Efficiency with Top-Notch Administrative Services"
    body = "I trust this message finds you well. I am reaching out to introduce you to Virtual World Services Limited, where we specialize in providing top-tier administrative solutions tailored to elevate businesses like yours. In today's dynamic business landscape, efficiency is key, and we are here to ensure your administrative tasks are handled seamlessly. Our team of skilled professionals excels in a wide range of services, including: Data Entry: Swift and accurate data entry to keep your records up-to-date.  Web Research: In-depth analysis for valuable insights into your industry. Extracting Email: Automate email extraction for efficient communication. Data Mining: Uncover valuable information to inform your business decisions. Data Scraping: Gather data from diverse sources for a comprehensive view. Lead Generation: Identify potential clients and opportunities to boost your sales. Email List Building: Construct targeted and responsive email lists for effective marketing. QuickBooks Data Entry: Precise financial record maintenance using QuickBooks. Bank Reconciliations: Ensure seamless alignment of your financial statements. Graphics Design: Eye-catching designs to enhance your brand presence. WordPress Customizing (WP Plugins): Tailor your website for a unique online presence. Typing (All formats): Fast and accurate typing services for all your documentation. Article Posting on WordPress: Keep your website content fresh and engaging. Email Sending: Strategic and efficient email campaigns to reach your audience. Spreadsheets: From data entry to formatting, we handle it all and more. Data Extraction Automation: Implement automated processes for efficient data retrieval. By partnering with Virtual World Services, you not only gain access to a diverse range of skills but also benefit from our commitment to quality and efficiency. Our goal is to contribute to your success by providing reliable and professional administrative support. If you're interested in learning more about how we can tailor our services to meet your specific needs, please don't hesitate to reach out. We would love to discuss how Virtual World Services can be a valuable asset to your business. Thank you for considering us, and we look forward to the opportunity to work with you. Jahangir Sheikh, Virtual World Services, WhatsApp: +8801710895569, Email: jahangir@virtualworld.services, Web: ttps://www.virtualworld.services/"
    send_email(to_email, to_name, subject, body)
    time.sleep(30)

    bounced_emails = check_bounced_emails(to_email)
    if to_email in bounced_emails:
        result = f"Email to {to_email} bounced or was blocked."
    else:
        result = f"Email to {to_email} delivered successfully."

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
