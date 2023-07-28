from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username


class Rating(models.Model):
    reviewer = models.ForeignKey(User, related_name='given_ratings', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_ratings', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=3, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        all_ratings = Rating.objects.filter(receiver=self.receiver)
        average_rating = all_ratings.aggregate(Avg('value'))['value__avg']
        profile = Profile.objects.get(user=self.receiver)
        profile.average_rating = average_rating
        profile.save()

    def __str__(self):
        return f'{self.reviewer.username} rated {self.receiver.username}'
