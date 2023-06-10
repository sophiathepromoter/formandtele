import logging
import requests
from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Telegram bot token
TOKEN = '6031687053:AAEzZ1dy3Z0Lxg4tl0VXm0a9NT2HJ_vpGog'

# SMTP server details
smtp_server = 'gmail'
smtp_port = 587
smtp_username = 'jd4946469@gmail.com'
smtp_password = 'nbtfuecckhgcltib'
sender_email = 'jd4946469@gmail.com'
receiver_email = 'jd4946469@gmail.com'

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

@app.route('/api/submit_form', methods=['POST'])
def submit_form():
    user_name = request.form.get('name')
    user_email = request.form.get('email')
    user_message = request.form.get('message')

    send_email(user_name, user_email)
    send_telegram_message(user_name, user_email, user_message)

    # You can process the user information or perform additional actions here

    return 'Form submitted successfully'

def send_email(user_name, user_email):
    """Send thank you email to the user."""
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Thank You'
    message['From'] = sender_email
    message['To'] = user_email

    text = f'Thank you, {user_name}, for submitting the form!'
    html = f'<p>Thank you, {user_name}, for submitting the form!</p>'

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, user_email, message.as_string())

def send_telegram_message(user_name, user_email, user_message):
    """Send user information to Telegram bot account."""
    bot_message = f"New form submission:\n\nName: {user_name}\nEmail: {user_email}\nMessage: {user_message}"
    bot_api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": "@sophiathepromoter",  # Replace with your Telegram chat ID
        "text": bot_message
    }
    response = requests.post(bot_api_url, data=data)
    if response.status_code == 200:
        logging.info('Telegram message sent successfully')
    else:
        logging.error('Error sending Telegram message')

if __name__ == '__main__':
    app.run()
