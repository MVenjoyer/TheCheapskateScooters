from datetime import datetime

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from web.models import Scooter, Rental


@csrf_exempt
@transaction.atomic
def rent_scooter(request, scooter_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Неверный метод запроса'})

    scooter = get_object_or_404(
        Scooter.objects.select_for_update(),
        id=scooter_id
    )

    if Rental.objects.filter(scooter=scooter, end_time__isnull=True).exists():
        return JsonResponse({'success': False, 'message': 'Самокат уже арендован'})

    rental = Rental.objects.create(
        user=request.user,
        scooter=scooter,
        start_time=datetime.now(),
        start_latitude=request.POST.get('lat'),
        start_longitude=request.POST.get('lng'),
    )

    scooter.is_available = False
    scooter.save(update_fields=['is_available'])

    return JsonResponse({
        'success': True,
        'message': 'Самокат успешно арендован',
        'rental_id': rental.id
    })


@csrf_exempt
@transaction.atomic
def cancel_rental(request, rental_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Неверный метод запроса'})

    try:
        rental = get_object_or_404(
            Rental.objects.select_for_update(),
            id=rental_id,
            user=request.user,
            end_time__isnull=True
        )

        scooter = rental.scooter

        rental.end_time = datetime.now()
        rental.end_latitude = request.POST.get('lat')
        rental.end_longitude = request.POST.get('lng')
        rental.is_cancelled = True
        rental.save()

        scooter.is_available = True
        scooter.save(update_fields=['is_available'])

        return JsonResponse({
            'success': True,
            'message': 'Аренда успешно отменена',
            'scooter_id': scooter.id
        })

    except Rental.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Аренда не найдена или у вас нет прав на её отмену'
        })
