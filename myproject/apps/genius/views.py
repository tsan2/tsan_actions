from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Action, User
from rest_framework import viewsets
from .serializers import ActionSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
