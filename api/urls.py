from django.db import router
from django.urls import path, include
from .views import MealViewSet, RatingViewSet, UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('meals', MealViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls))

]
