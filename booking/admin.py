from django.contrib import admin
from .models import *

admin.site.register(Location)
admin.site.register(Pitch)
admin.site.register(TimeSlot)
admin.site.register(Coupon)
admin.site.register(Booking)
admin.site.register(ReservedBooking)
