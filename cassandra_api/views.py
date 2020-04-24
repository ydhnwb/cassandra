from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from django.db.models import Q
from .serializers import *
from .models import *

class LoginViewSet(viewsets.ViewSet):
    serializer_class = AuthTokenSerializer

    def create(self, request):
        user = UserProfile.objects.filter(email = request.data.get('username')).first()
        if user is None:
            return Response({'message': 'No user found', 'status':False, 'data' : {}}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data = request.data, context={'request':request})
        if serializer.is_valid(raise_exception=False):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user = user)
            return Response({'message': 'Success', 'status':True, 'error':{}, 'data':{
                'id': user.id,
                'name': user.name,
                'email':user.email,
                'token':token.key
            }})
        return Response({'message':'Login failed', 'status':False,'error':{},'data':{}}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer

    def create(self, request):
        serializer = UserSerializer(data= request.data)
        if serializer.is_valid(raise_exception=False):
            user = UserProfile(email = serializer.data.get('email'),name = serializer.data.get('name'))
            user.set_password(request.data.get('password'))
            user.save()
            return Response({'message': 'Success', 'status':True,'error': {} ,'data':serializer.data})
        return Response({'message':'Register failed', 'status':False,'error':serializer.errors ,'data': {}}, status=status.HTTP_401_UNAUTHORIZED)

class TypeViewSet(viewsets.ViewSet):
    serializer_class = TypeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def create(self, request):
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            type = Type(name = request.data.get('type_name'), owner= request.user)
            type.save()
            return type
        return None

    def list(self, request):
        types = Type.objects.filter(owner = request.user).prefetch_related('plant')
        serializer = TypeSerializer(types, many=True)
        return Response({'message': 'Success', 'status': True, 'error': {}, 'data': serializer.data})

    def partial_update(self, request, pk= None):
        return Response({'message':'helllo wordl'})

    def get_or_create(self, name, owner):
        type = Type.objects.filter(Q(name__iexact=name) & Q(owner=owner)).first()
        if type is None:
            type = Type(name=name, owner=owner)
            type.save()
            return type
        return type

class LocationViewSet(viewsets.ViewSet):
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def create(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            location = Location(name=request.data.get('name'), owner=request.user)
            location.save()
            return location
        return None

    def get_or_create(self, name, owner):
        location = Location.objects.filter(Q(name__iexact=name) & Q(owner=owner)).first()
        if location is None:
            location = Location(name=name, owner=owner)
            location.save()
            return location
        return location

class PlantViewSet(viewsets.ViewSet):
    serializer_class = PlantSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def create(self, request):
        serializer = PlantPlainSerializer(data=request.data)
        if serializer.is_valid():
            location = LocationViewSet().get_or_create(request.data.get('location'), request.user)
            type = TypeViewSet().get_or_create(request.data.get('type'), request.user)
            plant = Plant(location = location, type = type, owner= request.user, name = request.data.get('name'),
                          description=request.data.get('description'), image=request.data.get('image'))
            plant.save()
            serializer = PlantSerializer(plant, many=False)
            return Response({'message':'Success creating plant!', 'status':True, 'error':{} ,'data': serializer.data})
        return Response({'message':'Failed to create plant', 'status':False,'error':serializer.errors, 'data':{} })

    def list(self, request):
        plants = Plant.objects.filter(owner = request.user)
        serializer = PlantSerializer(plants, many=True)
        return Response({'message': 'Here is your plants', 'status':False, 'error':{}, 'data':serializer.data})

    def retrieve(self, request, pk=None):
        pass