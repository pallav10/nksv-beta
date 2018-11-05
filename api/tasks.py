from celery import task
from django.core.mail import EmailMessage
from django.template.loader import get_template
from celery import shared_task


# @task(name='api.tasks.welcome_mail')
@shared_task(name='api.tasks.welcome_mail')
def welcome_mail(url_body, host_user, email):
    html_template = get_template('welcome_email_template.html')
    content_passed_to_template = {'url_body': url_body}
    html_content = html_template.render(content_passed_to_template)
    send_email = EmailMessage(
        'Welcome to Nakshatraveda',
        html_content,
        host_user,
        [email],
    )
    send_email.content_subtype = "html"
    send_email.send()
