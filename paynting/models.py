from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User


class Masterpiece(models.Model):
    masterpiece_name = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='media', blank=True)
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    made_with = models.OneToOneField('MadeWith', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.masterpiece_name

    def get_absolute_url(self):
        return reverse('masterpiece_detail', args=[str(self.id)])

    def save_user(self, user):
        self.uploaded_by = user

    def save_made_with(self, made_with):
        self.made_with = made_with

    class Meta:
        indexes = [
            models.Index(fields=['masterpiece_name', 'uploaded_by']),
        ]


class MadeWith(models.Model):
    hardware = models.CharField(max_length=1000, blank=True)
    software = models.CharField(max_length=1000, blank=True)


class Search(models.Model):
    search = models.CharField(max_length=500)

    def __str__(self):
        return self.search

    class Meta:
        verbose_name_plural = 'Searches'


class Sort(models.Model):
    SORT_TYPES = (
        ('az', 'A to Z'),
        ('za', 'Z to A'),
    )
    sort_type = models.CharField(max_length=2, choices=SORT_TYPES)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
