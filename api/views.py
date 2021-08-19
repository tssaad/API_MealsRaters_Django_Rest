from django.shortcuts import render
from rest_framework import serializers, viewsets
from .models import Rating, Meal
from .serializers import RatingSerializer, MealSerializer


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
