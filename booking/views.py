from .models import *
from .serializers import *
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework import filters as rest_framework_filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action


class LocationFilter(filters.FilterSet):
    class Meta:
        model = Location
        fields = {
            'name': ['icontains'],
            'locality': ['icontains'],
            'city': ['icontains'],
            'contact_person': ['icontains']
        }

class LocationViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Location.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    authentication_classes = [TokenAuthentication]
    filterset_class = LocationFilter
    filter_backends = [rest_framework_filters.SearchFilter, filters.DjangoFilterBackend, rest_framework_filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


class PitchFilter(filters.FilterSet):
    class Meta:
        model = Pitch
        fields = {
            'pitch_number': ['exact'],
            'location_id': ['exact'],
            'pitch_type': ['exact'],
            'starting_time': ['exact'],
            'ending_time': ['exact'],
            'status': ['exact']
        }


class PitchViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Pitch.
    """
    queryset = Pitch.objects.all()
    serializer_class = PitchSerializer
    authentication_classes = [TokenAuthentication]
    filterset_class = PitchFilter
    filter_backends = [rest_framework_filters.SearchFilter, filters.DjangoFilterBackend, rest_framework_filters.OrderingFilter]
    ordering_fields = ['pitch_type', 'pitch_number']
    ordering = ['-pitch_type', 'pitch_number']


class TimeSlotFilter(filters.FilterSet):
    class Meta:
        model = TimeSlot
        fields = {
            'slot_start_time': ['exact'],
            'slot_end_time': ['exact']
        }


class TimeSlotViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving TimeSlot.
    """
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    authentication_classes = [TokenAuthentication]
    filterset_class = TimeSlotFilter
    filter_backends = [rest_framework_filters.SearchFilter, filters.DjangoFilterBackend, rest_framework_filters.OrderingFilter]
    ordering_fields = ['slot_start_time']
    ordering = ['slot_start_time']


class CouponFilter(filters.FilterSet):
    class Meta:
        model = Coupon
        fields = {
            'coupon_code': ['exact'],
            'status': ['exact']
        }


class CouponViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Coupon.
    """
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    authentication_classes = [TokenAuthentication]
    filterset_class = CouponFilter
    filter_backends = [rest_framework_filters.SearchFilter, filters.DjangoFilterBackend, rest_framework_filters.OrderingFilter]
    ordering_fields = ['created_on']
    ordering = ['-created_on']


class BookingFilter(filters.FilterSet):
    class Meta:
        model = Booking
        fields = {
            'booking_date': ['exact'],
            'pitch_id': ['exact'],
            'pitch__location_id': ['exact'],
            'status': ['exact'],
            'booking_for': ['exact'],
            'booking_for__username': ['exact']
        }


class BookingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Booking.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    filterset_class = BookingFilter
    filter_backends = [rest_framework_filters.SearchFilter, filters.DjangoFilterBackend, rest_framework_filters.OrderingFilter]
    ordering_fields = ['booking_date']
    ordering = ['-booking_date']

    def create(self, request):
        data = request.data
        booking_date = data['booking_date'] if 'booking_date' in data else None
        pitch = data['pitch'] if 'pitch' in data else None
        time_slot = data['time_slot'] if 'time_slot' in data else None
        total_amount = data['total_amount'] if 'total_amount' in data else None
        applied_coupon = data['applied_coupon'] if 'applied_coupon' in data else None
        discount = data['discount'] if 'discount' in data else None
        net_amount = data['net_amount'] if 'net_amount' in data else None  
        paid_amount = data['paid_amount'] if 'paid_amount' in data else None  
        balance_amount = data['balance_amount'] if 'balance_amount' in data else None  
        booking_for = data['booking_for'] if 'booking_for' in data else None 
        created_by = data['created_by'] if 'created_by' in data else None  
        status = data['status'] if 'status' in data else None 

        pitch_instance = Pitch.objects.filter(id=pitch).first() 
        applied_coupon_instance = Coupon.objects.filter(id=applied_coupon).first()
        booking_for_instance = User.objects.filter(id=booking_for).first()
        created_by_instance = User.objects.filter(id=created_by).first()

        booking = Booking.objects.create(
                                booking_date=booking_date,
                                pitch=pitch_instance,
                                total_amount=total_amount,
                                applied_coupon=applied_coupon_instance,
                                discount=discount,
                                net_amount=net_amount,
                                paid_amount=paid_amount,
                                balance_amount=balance_amount,
                                booking_for=booking_for_instance,
                                status=status,
                                created_by=created_by_instance
                            )

        for slot in time_slot:
            slot_instance = TimeSlot.objects.get(id=slot)
            booking.time_slot.add(slot_instance)
        booking.save()
        return Response(status=201)

    @action(detail=False, methods=['GET'])
    def getpitchbookinglist(self, request):
        booking_date = request.query_params.get('booking_date', None)
        pitch = request.query_params.get('pitch', None)
        
        pitch_booking_list = Booking.objects.filter(pitch_id=pitch, booking_date=booking_date)
        serializer = BookingSerializer(pitch_booking_list, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def getfilteredbookinglist(self, request):
        booking_date = request.query_params.get('booking_date', None)
        location = request.query_params.get('location', None)

        if booking_date:
            if location: 
                booking_list = Booking.objects.filter(booking_date=booking_date, pitch__location_id=location)
            else:
                booking_list = Booking.objects.filter(booking_date=booking_date)
        else:
            if location: 
                booking_list = Booking.objects.filter(pitch__location_id=location)
            else:
                booking_list = Booking.objects.all()

        serializer = BookingSerializer(booking_list, many=True)
        return Response(serializer.data)
    

    def update(self, request, *args, **kwargs):
        status = request.data.pop('status', '')
        id = kwargs.pop('pk', 0)
        paid_amount = request.data.pop('paid_amount', None)
        balance_amount = request.data.pop('balance_amount', None)
        transaction_amount = request.data.pop('transaction_amount', None)
        modified_by = request.data.pop('modified_by', '')
        modified_by_user = User.objects.get(id=modified_by)

        if paid_amount:
            Booking.objects.filter(pk=id).update(paid_amount=paid_amount, balance_amount=balance_amount)
            booking = Booking.objects.get(pk=id)
            if booking.transactions=='null' or booking.transactions=='' or booking.transactions==None:
                transactions_list = []
                transactionstime = datetime.datetime.now() + datetime.timedelta(seconds=19800) # Adding 5:30 Hours 
                transactions_list.append({'amount': transaction_amount, 'paid_on': transactionstime.strftime("%Y-%m-%d %H:%M:%S")})
                transactionsdata = json.dumps(transactions_list, default=str)
                Booking.objects.filter(pk=id).update(transactions=transactionsdata)
            else:
                transactions_list = json.loads(booking.transactions)
                transactionstime = datetime.datetime.now() + datetime.timedelta(seconds=19800) # Adding 5:30 Hours 
                transactions_list.append({'amount': transaction_amount, 'paid_on': transactionstime.strftime("%Y-%m-%d %H:%M:%S")})
                transactionsdata = json.dumps(transactions_list, default=str)
                Booking.objects.filter(pk=id).update(transactions=transactionsdata)
        elif status and modified_by:
            Booking.objects.filter(pk=id).update(status=status, modified_by=modified_by_user)
        return Response(status=200)
    
    @action(detail=False, methods=['GET'])
    def getbookinglistbydaterange(self, request):
        range = request.query_params.get("range", "")
        if range == "Past Week":
            booking_list = Booking.objects.filter(booking_date__gte=datetime.datetime.now()-datetime.timedelta(days=15))
            print(booking_list)
        elif range == "Past Month":
            booking_list = Booking.objects.filter(booking_date__gte=datetime.datetime.now()-datetime.timedelta(weeks=4))
        elif range == "Past Year":
            booking_list = Booking.objects.filter(booking_date__gte=datetime.datetime.now()-datetime.timedelta(weeks=54))
        else:
            booking_list = Booking.objects.all()
        serializer = BookingSerializer(booking_list, many=True)
        return Response(serializer.data)





class ReservedBookingFilter(filters.FilterSet):
    class Meta:
        model = ReservedBooking
        fields = {
            'reserved_for': ['exact'],
            'reserved_for__username': ['exact'],
            'pitch_id': ['exact'],
            'pitch__location_id': ['exact'],
        }


class ReservedBookingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving ReservedBooking.
    """
    queryset = ReservedBooking.objects.all()
    serializer_class = ReservedBookingSerializer
    authentication_classes = [TokenAuthentication]
    filterset_class = ReservedBookingFilter
    filter_backends = [rest_framework_filters.SearchFilter, filters.DjangoFilterBackend, rest_framework_filters.OrderingFilter]
    ordering_fields = ['modified_on']
    ordering = ['-modified_on']

    @action(detail=False, methods=['GET'])
    def getreservedbookings(self, request):
        day = request.query_params.get('day', None)
        pitch = request.query_params.get('pitch', None)
        
        reserved_list = ReservedBooking.objects.filter(pitch_id=pitch, weekdays__icontains=day)
        serializer = ReservedBookingSerializer(reserved_list, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['POST'])
    def createreservation(self, request):
        reserved_for = request.data.pop('reserved_for', None)
        pitch = request.data.pop('pitch', None)
        time_slot = request.data.pop('time_slot', None)
        weekdays = request.data.pop('weekdays', None)
        exception_dates = request.data.pop('exception_dates', None)
        created_by = request.data.pop('created_by', None)

        reserved_for_instance = User.objects.get(id=reserved_for)
        pitch_instance = Pitch.objects.get(id=pitch)
        created_by_instance = User.objects.get(id=created_by)
        
        reservation = ReservedBooking.objects.create(
                                reserved_for=reserved_for_instance,
                                pitch=pitch_instance,
                                weekdays=weekdays,
                                exception_dates=exception_dates,
                                created_by=created_by_instance
                            )

        for slot in time_slot:
            slot_instance = TimeSlot.objects.get(id=slot)
            reservation.time_slot.add(slot_instance)
        reservation.save()
        return Response(status=201)