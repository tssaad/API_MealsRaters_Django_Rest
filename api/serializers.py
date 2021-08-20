from django.contrib.auth.models import User
from django.http import response
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from .models import Meal, Profile, Rating
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only':True, 'required':True}} # to stop showing password in json

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        token = Token.objects.create(user=user)
        response = {
            "message" : "User was created",
            "result" : token,
        }
        return Response(response, status=status.HTTP_201_CREATED)
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields = '__all__'
        
class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'title', 'description', 'number_of_ratings','avg_ratings']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'meal', 'user', 'stars']