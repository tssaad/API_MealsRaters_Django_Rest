#from django.shortcuts import render

from http.client import responses
from django.http import response
from django.http.request import RAISE_ERROR
from django.http.response import Http404
from django.contrib.auth.models import User

from rest_framework import serializers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from .models import Rating, Meal, Profile
from .serializers import RatingSerializer, MealSerializer, UserSerializer, ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        response = {
            "message" : "user was created",
            "token" : token.key
        }
        return Response(response, status=status.HTTP_201_CREATED)

    # in case you want to limit access when allowany
    def list(self, request, *args, **kwargs):
        response = {"message":"You cannnot create rating in here"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)



class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            # create or update
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']
            user=request.user
            #username = request.data['username'] # in case you don't have TOKEN 
            #user = User.objects.get(username=username)

            if int(stars) < 1 or int(stars) > 5:
                json = {
                    "message" : "stars are not in the allowed range. It must be between 1-5 only"
                }
                return Response(json, status=status.HTTP_400_BAD_REQUEST)

            try: # in case the rating exists
                rating = Rating.objects.get(meal=meal.id, user=user.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                json = {
                    'message' : 'Rating was updated!',
                    'result' : serializer.data,
                }
                return Response(json, status=status.HTTP_200_OK)
            except: # in case of new rating
                rating = Rating.objects.create(user=user, meal=meal, stars=stars)
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                json = {
                    'message' : 'Rating was added!',
                    'result' : serializer.data,
                }
                return Response(json, status=status.HTTP_200_OK)
        else:
            json = {
                "message" : "stars not provided"
            }
            return Response(json, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # if you want update and create to be only by meal not here 
    def update(self, request, *args, **kwargs):
        response = {
            "message" : "Update rating should not be here "
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {
            "message" : "Create rating should not be here "
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
