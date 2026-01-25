import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from web.models import Scooter,Rental

DEFAULT_PRICE_PER_MINUTE = 5
DEFAULT_BOARDER_FEE = 20
FIX_PRICE = 150

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
        user=request.user.profile,
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
    if request.method == 'POST':
        try:
            rental = get_object_or_404(
                Rental.objects.select_for_update(),
                id=rental_id,
                user=request.user.profile,
                end_time__isnull=True
            )
            scooter = rental.scooter

            try:
                data = json.loads(request.body)
                latitude = data.get('latitude')
                longitude = data.get('longitude')

                if latitude and longitude:
                    scooter.latitude = float(latitude)
                    scooter.longitude = float(longitude)
            except:
                pass
            rental.end_time = timezone.now()
            rental.end_latitude = request.POST.get('lat')
            rental.end_longitude = request.POST.get('lng')
            rental.is_cancelled = True

            scooter.is_available = True
            scooter.save(update_fields=['is_available'])
            if rental.end_time - rental.start_time >= timedelta(minutes=DEFAULT_BOARDER_FEE):
                duration_minutes = (rental.end_time - rental.start_time).total_seconds() / 60
                rental.total_price = FIX_PRICE + DEFAULT_BOARDER_FEE * duration_minutes
            else:
                rental.total_price = FIX_PRICE
            rental.save()
            return JsonResponse({
                'success': True,
                'message': f'Аренда завершена. Стоимость аренды: {format(rental.total_price)} руб.',
                'saved_coordinates': scooter.latitude is not None and scooter.longitude is not None
            })

        except Rental.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Аренда не найдена'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': 'Метод не разрешен'
    }, status=405)
