from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .forms import UserRegisterForm, LoginForm
from .models import Task, User, MyUser
from rest_framework import viewsets, permissions, status, mixins, generics
from .serializers import TaskSerializer, UserSerializer2, MyTokenObtainPairSerializer, UserSerializerMini, \
    UserSerializer, UserLoginSerializer, MegaTaskSerializer, TaskSerializerMini


class UserViewSet(UpdateModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
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

class UsersViewSetGetMe(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializerMini

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(email=request.user.email)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        a = serializer.save()
        return a

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task_this = self.perform_create(serializer)
        task_this.userFrom.add(request.user)
        ForUser = MyUser.objects.filter(id=request.data['userFor_id']).first()
        task_this.userFor.add(ForUser)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            userFrom = instance.userFrom
            for i in userFrom.all(): user_id_from = i.id

            userFor = instance.userFor
            for i in userFor.all(): user_id_for = i.id

            if instance.done == False and (user_id_from == request.user.id or user_id_for == request.user.id):
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                return Response({'status':200,
                                 'data':'task does not exist'})
        except Exception as e:
            if e == status.HTTP_404_NOT_FOUND:
                return Response({'status': 200,
                                 'data': 'task does not exist'})
            else:
                return Response({'status': 666,
                                 'data': 'error'})

    def list(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = instance.userFrom
            for i in user.all(): user_id = i.id
            if instance.done == False and user_id == request.user.id:
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'status':200,
                                 'data':'task does not exist'})
        except Exception as e:
            if e == status.HTTP_404_NOT_FOUND:
                return Response({'status': 200,
                                 'data': 'task does not exist'})
            else:
                return Response({'status': 666,
                                 'data': 'error'})

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            userFrom = instance.userFrom
            for i in userFrom.all(): user_id_from = i.id

            if instance.done == False and user_id_from == request.user.id:
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}

                return Response(serializer.data)
            else:
                return Response({'status': 200,
                                 'data': 'task does not exist'})
        except Exception as e:
            if e == status.HTTP_404_NOT_FOUND:
                return Response({'status': 200,
                                 'data': 'task does not exist'})
            else:
                return Response({'status': 666,
                                 'data': 'error'})

class TaskViewList(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MegaTaskSerializer

    def ListForMe(self, request, *args, **kwargs):
        queryset = Task.objects.filter(userFor=request.user).filter(done=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def ListForYou(self, request, *args, **kwargs):
        queryset = Task.objects.filter(userFrom=request.user).filter(done=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TaskDone(APIView):
    def post(self, request, task_id):
        task = Task.objects.filter(id=task_id).filter(userFor=request.user).filter(done=False)
        if task:
            FromUser = task.first().userFrom
            for i in FromUser.all():
                balance_from = i.balance

            FromUser.update(balance=balance_from+task.first().price)

            ForUser = task.first().userFor
            for i in ForUser.all():
                balance_for = i.balance

            FromUser.update(balance=balance_for - task.first().price)

            task.update(done=True)

            return Response({'status':200,
                             'data':'success'})
        else:
            return Response({'status':200,
                             'data':'task does not exist'})

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class MyTokenRefresh(TokenRefreshView):
    serializer_class = MyTokenObtainPairSerializer
