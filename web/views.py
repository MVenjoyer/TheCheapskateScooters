import json
import os

from django.db.models import Count, Prefetch, Q
from django.shortcuts import render, get_object_or_404
from .models import Scooter, ScooterPoint,Rental


YANDEX_API_KEY = os.getenv('YANDEX-API-KEY')

def home(request):
    available_scooters = Scooter.objects.filter(is_available=True)

    return render(request, 'home.html', {
        'scooters': available_scooters
    })


def map_view(request):
    points = ScooterPoint.objects.prefetch_related(
        Prefetch('scooters', queryset=Scooter.objects.filter(is_available=True),
                 to_attr='available_scooters')
    ).annotate(
        total_scooters=Count('scooters'),
        available_scooters=Count('scooters', filter=Q(scooters__is_available=True))
    ).order_by('-available_scooters')

    scooters = Scooter.objects.all()

    points_data = []
    for point in points:
        points_data.append({
            'id': point.id,
            'name': point.name,
            'latitude': float(point.latitude),
            'longitude': float(point.longitude),
        })

    scooters_data = []
    for scooter in scooters:
        scooters_data.append({
            'id': scooter.id,
            'name': scooter.name,
            'point_id': scooter.point.id if scooter.point else None,
            'latitude': float(scooter.point.latitude) if scooter.point else None,
            'longitude': float(scooter.point.longitude) if scooter.point else None,
            'is_available': scooter.is_available,
            'battery_level': scooter.battery_level,
            'rating': float(scooter.rating),
            'description': scooter.description or '',
        })

    return render(request, 'map.html', {
        'points': points,
        'scooters': scooters,
        'points_json': json.dumps(points_data),
        'scooters_json': json.dumps(scooters_data),
        'yandex_api_key': YANDEX_API_KEY,
    })


def point_detail(request, point_id):
    """Детальная страница точки с самокатами"""

    # Получаем точку с предзагрузкой самокатов
    point = get_object_or_404(
        ScooterPoint.objects.prefetch_related('scooters'),
        id=point_id
    )

    # Получаем все самокаты на точке
    all_scooters = point.scooters.all()

    # Доступные самокаты
    available_scooters = all_scooters.filter(is_available=True)

    # Фильтры из GET-параметров
    battery_min = request.GET.get('battery_min', 0)
    rating_min = request.GET.get('rating_min', 0)

    if battery_min:
        available_scooters = available_scooters.filter(
            battery_level__gte=int(battery_min)
        )

    if rating_min:
        available_scooters = available_scooters.filter(
            rating__gte=float(rating_min)
        )

    context = {
        'point': point,
        'all_scooters': all_scooters,
        'available_scooters': available_scooters,
        'total_count': all_scooters.count(),
        'available_count': available_scooters.count(),
    }

    return render(request, 'point_detail.html', context)

def rentals_view(request):
    user = request.user


    # Текущие аренды (еще не завершены)
    active_rentals = Rental.objects.filter(
        user=user,
        end_time__isnull=True
    ).select_related('scooter')


    # История аренд (уже завершены)
    past_rentals = Rental.objects.filter(
        user=user,
        end_time__isnull=False
    ).select_related('scooter').order_by('-end_time')


    context = {
        'active_rentals': active_rentals,
        'past_rentals': past_rentals,
    }


    return render(request, 'rentals.html', context)