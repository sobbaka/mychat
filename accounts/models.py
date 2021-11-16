from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.utils.html import mark_safe


class CustomUserManager(models.Manager):
    """Get CustomUser by username and email ???"""
    def get_by_natural_key(self, username, normalize_email):
        return self.get(username=username, normalize_email=normalize_email)


class CustomUser(AbstractUser):

    image = models.ImageField(verbose_name="Аватар", upload_to="covers/", null=True, blank=True)


    def natural_key(self):
        """Get username in serializer ???"""
        return self.username

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.id})

    def user_update(self):
        return reverse('user_update', kwargs={'pk': self.pk})

    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="50"/>'.format(self.image.url))
        return ""


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



