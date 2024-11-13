from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter


user_router = DefaultRouter()
user_router.register(r"", views.UserViewSet, basename="user")

role_router = DefaultRouter()
role_router.register(r"", views.RoleViewSet, basename="role")


urlpatterns = [
    path("login/", views.LoginView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("user/", include(user_router.urls)),
    path("role/", include(role_router.urls))
]