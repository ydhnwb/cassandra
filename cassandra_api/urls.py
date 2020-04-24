from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('login', LoginViewSet, basename='login')
router.register('register', RegisterViewSet, basename='register')
router.register('plant', PlantViewSet, basename='plant')
urlpatterns = [
    path('', include(router.urls))
]