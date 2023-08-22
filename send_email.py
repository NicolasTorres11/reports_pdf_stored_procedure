import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

smpt_server = 'mail.berlinasdelfonce.com'
smtp_port = 465
smtp_username = 'asistemas@berlinasdelfonce.com'
smtp_password = 'NUEVO*2023'
sender_mail = 'asistemas@berlinasdelfonce.com'
receiver_mail = 'asistemas@berlinasdelfonce.com'
subject = 'BERLINAS DEL FONCE S.A. --> Informe de Vencimientos de SOAT, RTM y Tarjetas de Operación'

dia_registro = datetime.datetime.now()

msg = MIMEMultipart()
msg['From'] = sender_mail
msg['To'] = receiver_mail
msg['Subject'] = subject

body = f"""
        <p>INFORME DE VENCIMIENTOS DE SOAT, RTM Y LAS TARJETAS DE OPERACION EN LOS VEHICULOS DE BOGOTA</p>
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

pdf_filename = 'vencimientosBogota.pdf'

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
