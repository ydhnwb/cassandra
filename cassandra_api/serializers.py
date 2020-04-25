from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'password', 'image')
        extra_kwargs = {'password': {'write_only': True}}

class LocationPlainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class TypePlainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class PlantSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    location =  LocationPlainSerializer(many=False)
    type = TypePlainSerializer(many=False)
    image = serializers.URLField(read_only=True, source='image.url')
    class Meta:
        model = Plant
        fields = '__all__'

class PlantPlainSerializer(serializers.ModelSerializer):
    location = serializers.CharField(write_only=True, required=True)
    type = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Plant
        fields = ('name', 'description', 'location', 'type', 'owner', 'image')
        extra_kwargs = {"owner": {"read_only": True}}


class LocationSerializer(serializers.ModelSerializer):
    plants = PlantSerializer(many=True, read_only=True)
    class Meta:
        model = Location
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    plants = PlantSerializer(many=True, read_only=True)
    class Meta:
        model = Type
        fields = '__all__'

class WateringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watering
        fields = '__all__'

class PruneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prune
        fields = '__all__'

class FertilizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fertilization
        fields = '__all__'