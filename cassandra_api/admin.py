from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Type)
admin.site.register(Location)
admin.site.register(Plant)
admin.site.register(Watering)
admin.site.register(Fertilization)
admin.site.register(Prune)
