# """
# URL configuration for myproject project.
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
import django
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from myproject.apps.genius.views import TaskViewSet, MyTokenObtainPairView, UserViewSet, UsersViewSetGet, \
    TokenRefreshView, UsersViewSetGetMe, TaskViewList, TaskDone
from rest_framework_swagger.views import get_swagger_view
from django.views.generic import TemplateView


# User_list = UserViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
# User_detail = UserViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })

User_list = UserViewSet.as_view({
     'post': 'create'
})

Users_list = UsersViewSetGet.as_view({
     'get': 'list'
})

Users_Me = UsersViewSetGetMe.as_view({
     'get': 'list'
})


Task_list = TaskViewSet.as_view({
    'post': 'create'
})

Task_list_me = TaskViewList.as_view({
    'get':'ListForMe'
})

Task_list_you = TaskViewList.as_view({
    'get':'ListForYou'
})

Task_detail = TaskViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

schema_view = get_schema_view(
    openapi.Info(
        title="tsan_actions_api",
        default_version='v0.1',
        description="API documentation",
        terms_of_service="<https://www.google.com/policies/terms/>",
        contact=openapi.Contact(email="nastabutcher.myasn@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('users/register/', User_list),
    path('users/list/', Users_list),
    path('users/me/', Users_Me),
    # path('login/', UserOperation.as_view({'post':'LoginView'})),
    # path('user/<int:pk>/', User_detail),
    path('api/token/', MyTokenObtainPairView.as_view()),
    path('api/refresh_token/', TokenRefreshView.as_view()),
    path('tasks/listMe/', Task_list_me),
    path('tasks/listYou/', Task_list_you),
    path('tasks/done/<int:task_id>/', TaskDone.as_view()),
    path('tasks/', Task_list),
    path('task/<int:pk>/', Task_detail)
]
