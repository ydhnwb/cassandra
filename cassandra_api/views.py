from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from .serializers import *
from .models import *
from .services import *

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

    def list(self, request):
        types = TypeService.all(request.user)
        serializer = TypeSerializer(types, many=True)
        return Response({'message': 'Success', 'status': True, 'error': {}, 'data': serializer.data})

    def partial_update(self, request, pk= None):
        return Response({'message':'helllo wordl'})

class LocationViewSet(viewsets.ViewSet):
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def list(self, request):
        locations = LocationService.all(request.user)
        serializer = LocationSerializer(locations, many=True)
        return Response({'message': 'Success', 'status': True, 'error': {}, 'data': serializer.data})


class PlantViewSet(viewsets.ViewSet):
    serializer_class = PlantSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def create(self, request):
        serializer = PlantPlainSerializer(data=request.data)
        if serializer.is_valid():
            location = LocationService.get_or_create(request.data.get('location'), request.user)
            type_plant = TypeService.get_or_create(request.data.get('type'), request.user)
            plant = PlantService.create_plant(request=request, location=location, type_plant=type_plant)
            serializer = PlantSerializer(plant, many=False)
            return Response({'message':'Success creating plant!', 'status':True, 'error':{} ,'data': serializer.data})
        return Response({'message':'Failed to create plant', 'status':False,'error':serializer.errors, 'data':{} })

    def list(self, request):
        plants = PlantService.all(request.user)
        serializer = PlantSerializer(plants, many=True)
        return Response({'message': 'Here is your plants', 'status':True, 'error':{}, 'data':serializer.data})

    def retrieve(self, request, pk=None):
        plant = PlantService.find_by_id(pk)
        if not plant:
            return Response({'message':'Data not found', 'status':False, 'error':{}, 'data': {}})
        serializer = PlantSerializer(plant, many=False)
        return Response({'message': 'Data not found', 'status': True, 'error': {}, 'data': serializer.data})

    def destroy(self, request, pk=None):
        plant = PlantService.find_by_id(pk)
        if not plant:
            return Response({'message': 'Data not found', 'status': False, 'error': {}, 'data': {}})
        plant.delete()
        PlantService.is_location_still_used(plant.location)
        PlantService.is_type_still_used(plant.type)
        return Response({'message': 'Success deleted', 'status': True, 'error': {}, 'data': {}})
