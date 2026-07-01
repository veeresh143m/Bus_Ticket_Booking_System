from django.contrib import admin
from .models import *

# Register your models here.
# class BusAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'source', 'destination', 'price')
# admin.site.register(User)
# admin.site.register(Bus)
# admin.site.register(Booking)

from django.contrib import admin
from .models import Bus, Seat, Booking, SeatLock


# 🚌 BUS ADMIN
class BusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'source', 'destination', 'price', 'total_seats')
    search_fields = ('name', 'source', 'destination')
    list_filter = ('source', 'destination')

    # 🔥 AUTO CREATE SEATS
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # create seats only if not exists
        if not Seat.objects.filter(bus=obj).exists():
            for i in range(1, obj.total_seats + 1):
                Seat.objects.create(bus=obj, seat_number=i)


# 🪑 SEAT ADMIN
class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'bus', 'seat_number', 'is_booked', 'is_locked')
    list_filter = ('bus', 'is_booked', 'is_locked')
    search_fields = ('seat_number',)


# 📦 BOOKING ADMIN
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bus', 'status', 'created_at')
    list_filter = ('status', 'bus')
    search_fields = ('user__username', 'passenger_name', 'mobile')
    readonly_fields = ('created_at',)


# 🔐 SEAT LOCK ADMIN
class SeatLockAdmin(admin.ModelAdmin):
    list_display = ('id', 'seat', 'user', 'locked_at')
    list_filter = ('locked_at',)


# REGISTER MODELS
admin.site.register(Bus, BusAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(SeatLock, SeatLockAdmin)