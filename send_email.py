import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

smpt_server = 'mail.berlinasdelfonce.com'
smtp_port = 465
smtp_username = 'asistemas@berlinasdelfonce.com'
smtp_password = 'NUEVO*2023'
sender_mail = 'asistemas@berlinasdelfonce.com'
receiver_mail = 'asistemas@berlinasdelfonce.com'
subject = 'PRUEBA'


msg = MIMEMultipart()
msg['From'] = sender_mail
msg['To'] = receiver_mail
msg['Subject'] = subject

body = 'PRUEBA ENVIO PDF'

pdf_filename = 'vencimientosBarranquilla.pdf'

with open(pdf_filename, 'rb') as pdf_file:
    pdf_attachment = MIMEApplication(pdf_file.read(), _subtype='pdf')
    pdf_attachment.add_header(
        'content-disposition', f'attachment; filename={pdf_filename}'
    )
    msg.attach(pdf_attachment)

try:
    with smtplib.SMTP_SSL(smpt_server, smtp_port) as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_mail, receiver_mail, msg.as_string())
    print('Correo Enviado Con exito!!!')
except Exception as e:
    print('Error al Enviar el Correo:', e)
