from django.urls import path

from .views import rent_scooter, cancel_rental

urlpatterns = [
    path('rent/<int:scooter_id>/', rent_scooter, name='rent_scooter'),
    path('de-rent/<int:rental_id>/', cancel_rental, name='de-rent_scooter'),
]
