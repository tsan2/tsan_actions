from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views import View
from django.views.generic import CreateView
from keyring import set_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .forms import UserRegisterForm, LoginForm
from .models import Action, User, MyUser
from rest_framework import viewsets, permissions, status, mixins, generics
from .serializers import ActionSerializer, UserSerializer2, MyTokenObtainPairSerializer, UserSerializerMini, UserSerializer, UserLoginSerializer

class UserViewSet(UpdateModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # user = request.data.get('user', {})
        # serializer = self.serializer_class(data=user)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        new_user = User.objects.create_user(email=request.data['email'], name=request.data['name'], password=request.data['password'])
        return Response(request.data)

class UsersViewSetGet(mixins.ListModelMixin, GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        if user.is_superuser:
            return UserSerializer2
        else:
            return UserSerializerMini
#
# class
# def UserMeInfo(request):
#     Info = User.objects.filter(email=request.user.email)
#     qs_json = serializers.serialize('json', Info.all())
#     return JsonResponse({'user': qs_json})


#
# class UserOperation(GenericViewSet):

#     serializer_class = UserLoginSerializer
#     def LoginView(self, request):
#         email = request.data['email']
#         password = request.data['password']
#         user = authenticate(username=email, password=password)
#         if user is not None:
#             print(request)
#             login(request, user)
#             self.request.session["authenticated"] = True
#             return Response({'status_code': '200',
#                 'info': 'success'})
#         else:
#             return Response({'status_code': '400',
#                     'info': 'error'})
#


class UsersViewSetGetMe(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializerMini

    # def list(self, request, *args, **kwargs):
    #     Info = User.objects.filter(email=request.user.email).values()
    #     return JsonResponse({'user': list(Info)})
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(email=request.user.email)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ActionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        print(request.data)
        b = request.data.copy()
        b['user'] = request.user
        # a = QueryDict({**request.data, ** {'user':request.user}})
        # print(a)
        serializer = self.get_serializer(data=b)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# class UserView(mixins.CreateModelMixin):
#     form_class = UserCreationForm
#
#     def create(self, request, **extra_fields):
#         new_user = User.objects.create_user(request.user.name, request.user.password)
#         return new_user

class MyTokenRefresh(TokenRefreshView):
    serializer_class = MyTokenObtainPairSerializer
