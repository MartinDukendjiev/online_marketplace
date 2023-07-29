from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from online_marketplace import settings

UserModel = get_user_model()


def sand_successful_registration_email(user):
    html_message = render_to_string(
        'emails/email-greeting.html',
        {'user': user}
    )

    plain_massage = strip_tags(html_message)  # removes tags and shows only the text of the HTML

    send_mail(

        subject='Successful Registration',
        message=plain_massage,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(user.email,)
    )


@receiver(post_save, sender=UserModel)
def user_created(instance, created, **kwargs):
    if created:
        sand_successful_registration_email(instance)
