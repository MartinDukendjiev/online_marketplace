from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.contrib.auth.models import AbstractUser
from django.db import models

from online_marketplace.common.validators import image_size_validator_5mb


class MarketplaceUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        validators=[image_size_validator_5mb],
    )
    average_rating = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)


class Rating(models.Model):
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='given_ratings',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_ratings',
        on_delete=models.CASCADE
    )
    value = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(5, message="Value must be less than or equal to 5"),
            MinValueValidator(1, message="Value must be greater than or equal to 1")
        ]
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        all_ratings = Rating.objects.filter(receiver=self.receiver)
        average_rating = all_ratings.aggregate(Avg('value'))['value__avg']
        profile = MarketplaceUser.objects.get(id=self.receiver.id)
        profile.average_rating = average_rating
        profile.save()

    def __str__(self):
        return f'{self.reviewer.username} rated {self.receiver.username}'


class Comment(models.Model):
    user = models.ForeignKey(MarketplaceUser, on_delete=models.CASCADE)
    seller_profile = models.ForeignKey(MarketplaceUser, related_name='comments_received', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.seller_profile.username} profile'
