from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('login', LoginViewSet, basename='login')
router.register('register', RegisterViewSet, basename='register')
router.register('plant', PlantViewSet, basename='plant')
router.register('location', LocationViewSet, basename='location')
router.register('type', TypeViewSet, basename='type')
urlpatterns = [
    path('', include(router.urls))
]