import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def enviar_correo(destinatario, asunto, cuerpo, adjunto=None):
    smtp_server = 'tu_servidor_smtp'
    puerto = 587
    usuario = 'tu_correo@gmail.com'
    contraseña = 'tu_contraseña'

    mensaje = MIMEMultipart()
    mensaje['From'] = usuario
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    mensaje.attach(MIMEText(cuerpo, 'plain'))

    if adjunto:
        with open(adjunto, "rb") as archivo:
            adjunto_mime = MIMEApplication(archivo.read(), _subtype="xlsx")
            adjunto_mime.add_header('Content-Disposition', f'attachment; filename={adjunto}')
            mensaje.attach(adjunto_mime)

    with smtplib.SMTP(smtp_server, puerto) as server:
        server.starttls()
        server.login(usuario, contraseña)
        server.sendmail(usuario, destinatario, mensaje.as_string())

if __name__ == "__main__":
    destinatario = 'destinatario@example.com'
    asunto = 'Asunto del correo'
    cuerpo = 'Cuerpo del correo'

    adjunto = 'reporte.xlsx'

    enviar_correo(destinatario, asunto, cuerpo, adjunto)
