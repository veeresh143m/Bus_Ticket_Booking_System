from rest_framework import generics
from .models import Bus, Booking
from .serializers import BusSerializer, BookingSerializer


class BusListAPIView(generics.ListAPIView):
    queryset = Bus.objects.all().order_by('source', 'destination')
    serializer_class = BusSerializer


class BusDetailAPIView(generics.RetrieveAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer


class BookingListAPIView(generics.ListAPIView):
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingSerializer
