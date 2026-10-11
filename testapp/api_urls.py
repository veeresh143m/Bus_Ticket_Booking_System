from django.urls import path
from .api_views import BusListAPIView, BusDetailAPIView, BookingListAPIView

urlpatterns = [
    path('buses/', BusListAPIView.as_view(), name='api_bus_list'),
    path('buses/<int:pk>/', BusDetailAPIView.as_view(), name='api_bus_detail'),
    path('bookings/', BookingListAPIView.as_view(), name='api_booking_list'),
]
