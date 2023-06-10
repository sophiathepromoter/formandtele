from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/api/submit_form', methods=['POST'])
def submit_form():
    user_name = request.form.get('name')
    user_email = request.form.get('email')
    user_message = request.form.get('message')

    send_email(user_name, user_email)

    # You can process the user information or perform additional actions here

    return 'Form submitted successfully'

def send_email(user_name, user_email):
    """Send thank you email to the user."""
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Thank You'
    message['From'] = 'your-sender-email'
    message['To'] = user_email

    text = f'Thank you, {user_name}, for submitting the form!'
    html = f'<p>Thank you, {user_name}, for submitting the form!</p>'

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP('your-smtp-server', 587) as server:
        server.starttls()
        server.login('your-smtp-username', 'your-smtp-password')
        server.sendmail('your-sender-email', user_email, message.as_string())

if __name__ == '__main__':
    app.run()
