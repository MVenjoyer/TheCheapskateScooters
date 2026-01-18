from django.contrib import admin
from .models import ScooterPoint, Scooter


@admin.register(ScooterPoint)
class ScooterPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'scooters_count')
    search_fields = ('name',)

    def scooters_count(self, obj):
        return obj.scooters.count()

    scooters_count.short_description = 'Количество самокатов'


@admin.register(Scooter)
class ScooterAdmin(admin.ModelAdmin):
    list_display = ('name', 'point', 'rating', 'battery_level', 'is_available')
    list_filter = ('is_available', 'rating', 'point')
    search_fields = ('name', 'description')

    readonly_fields = ('location_display', 'created_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'point')
        }),
        ('Статус', {
            'fields': ('is_available', 'rating', 'battery_level')
        }),
        ('Дополнительно', {
            'fields': ('location_display',),
            'classes': ('collapse',)
        }),
    )

    def location_display(self, obj):
        if obj.point:
            return f"Широта: {obj.point.latitude}, Долгота: {obj.point.longitude}"
        return "Не указана"

    location_display.short_description = 'Координаты'
