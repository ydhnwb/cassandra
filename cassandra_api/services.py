from django.db.models import Q
from .models import *

class PlantService(object):

    @staticmethod
    def create_plant(request, location, type_plant):
        plant = Plant(location=location, type=type_plant, owner=request.user, name=request.data.get('name'),description=request.data.get('description'), image=request.data.get('image'))
        plant.save()
        return plant

    @staticmethod
    def all(user):
        plants = Plant.objects.filter(owner= user)
        return plants

    @staticmethod
    def find_by_id(plant_id):
        plant = Plant.objects.filter(id = plant_id).first()
        return plant

    @staticmethod
    def find_by_location(location):
        plants = Plant.objects.filter(location=location)
        return plants

    @staticmethod
    def find_by_type(plant_type):
        plants = Plant.objects.filter(type=plant_type)
        return plants

    @staticmethod
    def is_location_still_used(location):
        plants = PlantService.find_by_location(location)
        if not plants.exists():
            LocationService.destroy(location.id)
            return False
        return True

    @staticmethod
    def is_type_still_used(plant_type):
        plants = PlantService.find_by_type(plant_type)
        if not plants.exists():
            LocationService.destroy(plant_type.id)
            return False
        return True


class LocationService:

    @staticmethod
    def all(user):
        locations = Location.objects.prefetch_related('plants')
        return locations

    @staticmethod
    def get_or_create(name, owner):
        location = Location.objects.filter(Q(name__iexact=name) & Q(owner=owner)).first()
        if location is None:
            location = Location(name=name, owner=owner)
            location.save()
            return location
        return location

    @staticmethod
    def destroy(location_id):
        Location.objects.delete(id = location_id)
        return True

class TypeService:

    @staticmethod
    def all(user):
        types = Type.objects.filter(owner = user).prefetch_related('plant')
        return types


    @staticmethod
    def get_or_create(name, owner):
        type_plant = Type.objects.filter(Q(name__iexact=name) & Q(owner=owner)).first()
        if type_plant is None:
            type_plant = Type(name=name, owner=owner)
            type_plant.save()
            return type_plant
        return type_plant
