from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from .models import Application

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=Application)
def notify_user_selection(sender, instance, created, **kwargs):
    if not created and instance.status == 'selected':
        send_mail(
            subject="Congratulations! You have been selected",
            message=f"You have been selected for {instance.job or instance.internship}.",
            from_email="admin@jobmarketplace.com",
            recipient_list=[instance.user.email],
        )