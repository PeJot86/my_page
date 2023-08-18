import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_from_page(mail_name, mail_from, mail_subject, mail_message):
    msg = MIMEMultipart()
    msg['From'] = mail_from
    msg['To'] = 'webmaster@godsoftdev.com'
    msg['Subject'] = f"Wiadomość od {mail_name}"
    message = f"{mail_subject}\n\n{mail_message}\n\npozdrawiam {mail_name}\n\n{mail_from}"
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('mail37.mydevil.net',587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login('webmaster@godsoftdev.com', 'MixFix2012!')
    mailserver.sendmail('webmaster@godsoftdev.com', 'webmaster@godsoftdev.com', msg.as_string())
    mailserver.quit()
    return print("Wysłano")





