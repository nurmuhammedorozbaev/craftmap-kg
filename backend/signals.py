from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile


# --- Автоматическое создание профиля ---
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# --- Автоматическое сохранение профиля ---
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # если профиль существует — сохраняем
    if hasattr(instance, "profile"):
        instance.profile.save()
