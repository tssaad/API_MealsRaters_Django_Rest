from django.db import router
from django.urls import path, include
from .views import MealViewSet, RatingViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('meals', MealViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls))

]
