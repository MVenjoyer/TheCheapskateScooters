from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )

    def __str__(self):
        return f'{self.user.username} - {self.phone}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class ScooterPoint(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название точки")
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Точка самоката"
        verbose_name_plural = "Точки самокатов"


class Scooter(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")
    is_available = models.BooleanField(default=True, verbose_name="Доступен")
    battery_level = models.IntegerField(default=100, verbose_name="Уровень батареи")
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    point = models.ForeignKey(
        ScooterPoint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='scooters',
        verbose_name="Точка расположения"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-rating']
        verbose_name = "Самокат"
        verbose_name_plural = "Самокаты"

    @property
    def location(self):
        if self.point:
            return f"{self.point.latitude}, {self.point.longitude}"
        return ""

class Rental(models.Model):
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='rentals'
    )
    scooter = models.ForeignKey(
        'Scooter',
        on_delete=models.CASCADE,
        related_name='rentals'
    )

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    start_latitude = models.FloatField(null=True, blank=True)
    start_longitude = models.FloatField(null=True, blank=True)

    end_latitude = models.FloatField(null=True, blank=True)
    end_longitude = models.FloatField(null=True, blank=True)

    total_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['user', 'end_time']),
            models.Index(fields=['scooter', 'end_time']),
        ]

    def __str__(self):
        status = 'ACTIVE' if self.end_time is None else 'FINISHED'
        return f'Rental #{self.id} — {self.scooter} ({status})'

    @property
    def is_active(self):
        return self.end_time is None