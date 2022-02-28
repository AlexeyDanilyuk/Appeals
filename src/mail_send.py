import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(recipient, subj, body):
    server = 'smtp.mail.ru'
    sender = 'address_sender@mail.ru'
    password = '%^bd%bd5Db5N6d'

    text = body
    html = '<html><head></head><body><p>' + text + '</p></body></html>'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subj
    # msg['From'] = 'Система обработки обращений МС ХК'
    msg['To'] = recipient

    part_text = MIMEText(text, 'plain')
    part_html = MIMEText(html, 'html')

    msg.attach(part_text)
    msg.attach(part_html)

    mail = smtplib.SMTP_SSL(server)
    mail.login(sender, password)
    mail.sendmail(sender, recipient, msg.as_string())
    mail.quit()
