import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(user, pwd, recipient, subject, body):
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, pwd)
    server.send_message(msg)
    server.quit()

# 사용 예시
send_email('your_email@gmail.com', 'your_password', 'recipient_email@gmail.com', 'Hello', 'This is a test email.')
