from django.urls import path

from web.views import home, map_view, point_detail, rentals_view

urlpatterns = [
    path('', home, name='home'),
    path('map', map_view, name='map'),
    path('points/<int:point_id>/', point_detail, name='point_detail'),
    path('rentals/', rentals_view, name='rentals'),
]
