# valentine_contest/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_verification_email_task(recipient_email, verification_url):
    """
    Tarea asíncrona para enviar el correo de verificación.
    Recibe el email del destinatario y la URL de verificación completa.
    """
    subject = 'Verifica tu cuenta para participar en el sorteo de San Valentín'
    message = f'Hola,\n\nHaz clic en el siguiente enlace para verificar tu cuenta y crear tu contraseña: {verification_url}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

@shared_task
def send_winner_notification_task(recipient_email, full_name):
    """
    Tarea asíncrona para enviar el correo de notificación al ganador.
    Recibe el email del ganador y su nombre completo.
    """
    subject = '¡Felicidades, eres el ganador del sorteo de San Valentín!'
    message = f'¡Enhorabuena, {full_name}! Has ganado una estadía de 2 noches en nuestro hotel. Te contactaremos pronto con los detalles.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)