import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def Send_Email(user, pwd, recipient, subject, body):
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, pwd)
    text = msg.as_string()
    server.sendmail(user, recipient, text)
    server.quit()
    
    
