import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_email(pdf_filename, ciudad, recipient_emails):
    smpt_server = 'mail.berlinasdelfonce.com'
    smtp_port = 465
    smtp_username = 'asistemas@berlinasdelfonce.com'
    smtp_password = 'NUEVO*2023'
    sender_mail = 'asistemas@berlinasdelfonce.com'
    # receiver_mail = 'asistemas@berlinasdelfonce.com'
    # receiver_2 = 'sistemas@berlinasdelfonce.com'
    subject = 'BERLINAS DEL FONCE S.A. --> Informe de Vencimientos de SOAT, RTM y Tarjetas de Operación'

    dia_registro = datetime.datetime.now()

    msg = MIMEMultipart()
    msg['From'] = sender_mail
    recipients = ', '.join(recipient_emails)
    msg['To'] = recipients
    msg['Subject'] = subject

    body = f"""
            <p>INFORME DE VENCIMIENTOS DE SOAT, RTM Y LAS TARJETAS DE OPERACION EN LOS VEHICULOS DE {ciudad}</p>
            <br/>
            Adjunto al presente estamos enviando el detalle del Informe de Vencimientos de SOAT, RTM y Tarjetas de Operación:<br/>
            <br/>
            Fecha de Movimiento: {dia_registro:%Y-%m-%d %H:%M:%S}<br/>
            <br/>
            Cordialmente,<br/>
            <br/>
            Monica Pulido Molina<br/>
            Asistente Administrativa<br/>
            <a href="mailto:tramitesvehiculos@berlinasdelfonce.com">tramitesvehiculos@berlinasdelfonce.com</a><br/>
            <a href="http://www.berlinasdelfonce.com">www.berlinasdelfonce.com</a><br/>
            Teléfono: (60-1) 7435050 Ext 1201<br/>
            Oficina Principal: Cra 68D No. 15 - 15<br/>
            Bogota-Colombia<br/>
            """
    msg.attach(MIMEText(body, "html"))

    with open(pdf_filename, 'rb') as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read(), _subtype='pdf')
        pdf_attachment.add_header(
            'content-disposition', f'attachment; filename={pdf_filename}'
        )
        msg.attach(pdf_attachment)

    try:
        with smtplib.SMTP_SSL(smpt_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_mail, recipient_emails, msg.as_string())
        print('Correo Enviado Con exito!!!')
    except Exception as e:
        print('Error al Enviar el Correo:', e)


data = [
    ('vencimientosBarranquilla.pdf', 'BARRANQUILLA', [
     'asistemas@berlinasdelfonce.com', 'penatorresnicolas@gmail.com']),
    ('vencimientosBogota.pdf', 'BOGOTA', [
     'sistemas@berlinasdelfonce.com', 'penatorresnicolas@gmail.com'])
]

for pdf_file, city, recipient_email in data:
    send_email(pdf_file, city, recipient_email)
