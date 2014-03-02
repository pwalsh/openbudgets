# import datetime
# from django.core.mail import send_mail
# from celery import shared_task


#@shared_task(name="tasks.send_notification")
#def send_notification():
#
#    subject = ''
#    message = ''
#    sender = ''
#    recipient = ''
#
#    send_response = send_mail(
#        subject,
#        message,
#        sender,
#        [recipient],
#        fail_silently=True
#    )
