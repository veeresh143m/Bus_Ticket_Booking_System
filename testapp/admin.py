from django.contrib import admin
from .models import *

# Register your models here.
class BusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'source', 'destination', 'price')
admin.site.register(User)
admin.site.register(Bus)
admin.site.register(Booking)