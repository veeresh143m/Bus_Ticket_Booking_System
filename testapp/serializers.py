from rest_framework import serializers
from .models import Bus, Booking, Seat


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'is_booked', 'is_locked']


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['id', 'name', 'source', 'destination', 'price', 'total_seats']


class BookingSerializer(serializers.ModelSerializer):
    bus = BusSerializer(read_only=True)
    seats = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'bus', 'seats', 'passenger_name', 'mobile', 'status', 'created_at']
