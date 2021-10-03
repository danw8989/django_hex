from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import BooleanField, CharField, DateTimeField, DurationField, IntegerField, URLField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class PlanInfo(models.Model):
    thumbnail_height = IntegerField(default=200, validators=[MaxValueValidator(800), MinValueValidator(16)])
    thumbnail_width = IntegerField(null=True, validators=[MaxValueValidator(800), MinValueValidator(16)])
    original_link = BooleanField(default=False)
    expired_link = BooleanField(default=False)


class Plan(models.Model):
    name = CharField(max_length=30)
    plan_info = ForeignKey(PlanInfo, on_delete=models.CASCADE)


class ImageInfo(models.Model):
    LINK_TYPE = ['Thumbnail', 'Expiring']
    link = URLField()
    type = CharField(choices=LINK_TYPE, default='Thumbnail')
    expiring = DateTimeField()


class Image(models.Model):
    image = ImageField(upload_to='media')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = ForeignKey(User, on_delete=models.CASCADE)

class UserPlan(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    plan = ForeignKey(Plan, default=1)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserPlan.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
