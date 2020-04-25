from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils import timezone

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password = None):
        if not email:
            raise ValueError("The user must have an email address")

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        email = self.normalize_email(email)
        user = self.model(email = email, name = name)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using = self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, validators=[MinLengthValidator(4)])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    image = models.ImageField(default="https://miro.medium.com/max/560/1*MccriYX-ciBniUzRKAUsAw.png", null=True)
    password = models.CharField(max_length=255,validators=[MinLengthValidator(8)])
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_user(self):
        return UserProfile(email= self.email, name = self.name, image_url = self.image)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

class Type(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    owner = models.ForeignKey(UserProfile, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    owner = models.ForeignKey(UserProfile, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class Plant(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='plants')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='plants')
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=False, null=True, default=None, upload_to='plants')

    def __str__(self):
        return self.name

class Watering(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='watering')
    water_time = models.TimeField(null = False, blank=False)
    last_watered = models.DateTimeField(null=True, blank=False)
    remind_in_day = models.IntegerField(default=1, blank=False, null=False)

    def __str__(self):
        return "{0} - {1}".format(self.plant.name, "watered")


class Fertilization(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='fertilization')
    fertilize_time = models.TimeField(null = False, blank=False)
    last_fertilized = models.DateTimeField(null=True, blank=False)
    remind_in_day = models.IntegerField(default=1, blank=False, null=False)

    def __str__(self):
        return "{0} - {1}".format(self.plant.name, "fertilized")

class Prune(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='prune')
    prune_time = models.TimeField(null = False, blank=False)
    last_pruned = models.DateTimeField(null=True, blank=False)
    remind_in_day = models.IntegerField(default=1, blank=False, null=False)

    def __str__(self):
        return "{0} - {1}".format(self.plant.name, "pruned")
