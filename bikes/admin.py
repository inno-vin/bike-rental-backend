from django.contrib import admin
from .models import Bike


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'price_per_day')
    search_fields = ('title', 'owner__username')
