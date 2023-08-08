from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from online_marketplace import settings

UserModel = get_user_model()


def send_successful_registration_email(user):
    html_message = render_to_string(
        'emails/email-greeting.html',
        {'user': user}
    )

    plain_message = strip_tags(html_message)
    send_mail(
        subject='Successful Registration',
        message=plain_message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(user.email,)
    )


@receiver(post_save, sender=UserModel)
def user_created(instance, created, **kwargs):
    if created:
        send_successful_registration_email(instance)


@receiver(post_migrate, sender='online_marketplace.products')
def add_user_groups(sender, **kwargs):
    content_type_product = ContentType.objects.get(app_label='products', model='product')
    content_type_category = ContentType.objects.get(app_label='products', model='category')
    content_type_product_image = ContentType.objects.get(app_label='products', model='productimage')

    content_types = [content_type_product, content_type_category, content_type_product_image]
    staff_permissions = Permission.objects.filter(content_type__in=content_types)

    staff_group, created = Group.objects.get_or_create(name='Staff')
    if created or not created:
        existing_permissions = list(staff_group.permissions.all())
        staff_group.permissions.set(existing_permissions + list(staff_permissions))
