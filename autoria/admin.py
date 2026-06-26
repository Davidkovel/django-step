from django.contrib import admin

from .models import Car, Favorite


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price_usd', 'city', 'created_at')
    list_filter = ('transmission', 'body_type', 'city')
    search_fields = ('brand', 'model', 'city', 'plate', 'vin')
    readonly_fields = ('created_at', 'posted', 'price_uah')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'car__brand', 'car__model')
    readonly_fields = ('created_at',)
