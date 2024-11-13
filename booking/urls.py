from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter


location_router = DefaultRouter()
location_router.register(r"", views.LocationViewSet, basename="location")

pitch_router = DefaultRouter()
pitch_router.register(r"", views.PitchViewSet, basename="pitch")

timeslot_router = DefaultRouter()
timeslot_router.register(r"", views.TimeSlotViewSet, basename="timeslot")

coupon_router = DefaultRouter()
coupon_router.register(r"", views.CouponViewSet, basename="coupon")

booking_router = DefaultRouter()
booking_router.register(r"", views.BookingViewSet, basename="booking")

reserved_booking_router = DefaultRouter()
reserved_booking_router.register(r"", views.ReservedBookingViewSet, basename="reserved_booking")


urlpatterns = [
    path("location/", include(location_router.urls)),
    path("pitch/", include(pitch_router.urls)),
    path("timeslot/", include(timeslot_router.urls)),
    path("coupon/", include(coupon_router.urls)),
    path("booking/", include(booking_router.urls)),
    path("reservedbooking/", include(reserved_booking_router.urls)),
]