from django.contrib import admin
from .models import UserProfile, Car


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'license_number', 'created_at']
    search_fields = ['user__username', 'user__email', 'license_number']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'plate_number', 'daily_rate', 'status']
    list_filter = ['status', 'brand']
    search_fields = ['brand', 'model', 'plate_number']
