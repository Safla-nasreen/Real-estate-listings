from django.contrib import admin
from .models import Location, PropertyType, Property, Cart, CartItem, Payment

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'State', 'country')
    search_fields = ('city', 'State', 'country')

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'property_type', 'bedrooms', 'bathrooms')
    search_fields = ('title', 'address', 'location__city', 'property_type__name')
    list_filter = ('property_type', 'location', 'bedrooms', 'bathrooms')
    raw_id_fields = ('location', 'property_type')

