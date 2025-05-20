from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserInfo
from .utils import load_music_from_file
from DjangoProject.settings import ADMIN_PASSWORD, ADMIN_USERNAME, ADMIN_EMAIL


@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)



@receiver(post_migrate,  dispatch_uid="create_music_post_migrate")
def create_music(sender, **kwargs):
    load_music_from_file()



@receiver(post_migrate,  dispatch_uid="create_default_admin_account")
def create_default_admin_account(sender, **kwargs):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(f'{ADMIN_USERNAME}',f'{ADMIN_EMAIL}', f'{ADMIN_PASSWORD}')