from django.contrib import admin
from .models import Meal, Rating, Profile

admin.site.register(Profile)

class AdminMeal(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    search_fields = ['title', 'description']
    list_filter = ['title', 'description']

admin.site.register(Meal, AdminMeal)

class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'meal', 'user', 'stars']
    list_filter = ['meal', 'user']
    
admin.site.register(Rating)