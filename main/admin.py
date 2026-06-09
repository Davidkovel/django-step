from django.contrib import admin
from .models import Car, CarPhoto, SavedCar


class CarPhotoInline(admin.TabularInline):
    model = CarPhoto
    extra = 3


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'price_usd', 'city', 'seller', 'created_at', 'is_verified']
    list_filter = ['brand', 'fuel', 'transmission', 'is_verified', 'year']
    search_fields = ['brand', 'model', 'vin_code', 'license_plate']
    inlines = [CarPhotoInline]
    readonly_fields = ['views_count', 'created_at', 'updated_at']


@admin.register(CarPhoto)
class CarPhotoAdmin(admin.ModelAdmin):
    list_display = ['car', 'is_main', 'order']


@admin.register(SavedCar)
class SavedCarAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'saved_at']