from enum import unique
from django.core import validators
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.base import Model

#uuid

class Meal(models.Model):
    title       = models.CharField(max_length=32)
    description = models.TextField()

    def number_of_ratings(self):
        ratings = Rating.objects.filter(meal=self)
        return len(ratings)

    def avg_ratings(self):
        ratings = Rating.objects.filter(meal=self)
        if len(ratings):
            sum=0
            for r in ratings:
                sum +=r.stars
            avg = sum / len(ratings)
        else:
            avg=0
        return avg

    def __str__(self):
        return self.title

class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return str(self.stars)

    class Meta:
        unique_together = (('user', 'meal'),) # only one time rating 
        index_together = (('user', 'meal'),)