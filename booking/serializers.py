from rest_framework import serializers
from .models import *
from account.serializers import UserSerializer

class LocationSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all(), allow_null=True)
    created_by_data = UserSerializer(required=False, allow_null=True)

    modified_by = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all(), allow_null=True)
    modified_by_data = UserSerializer(required=False, allow_null=True)

    image_1 = serializers.ImageField(required=False)
    image_2 = serializers.ImageField(required=False)
    image_3 = serializers.ImageField(required=False)
    image_4 = serializers.ImageField(required=False)
    image_5 = serializers.ImageField(required=False)

    class Meta:
        model = Location
        fields = (
            "id",
            "name",
            "address",
            "locality",
            "city",
            "state",
            "contact_person",
            "contact_number",
            "image_1",
            "image_2",
            "image_3",
            "image_4",
            "image_5",

            #Statistics
            "created_on",
            "created_by",
            "created_by_data",
            "modified_on",
            "modified_by",
            "modified_by_data"
        )
        read_only_fields = ["id", "created_on", "created_by"]

    def create(self, validated_data):
        instance = Location(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.locality = validated_data.get("locality", instance.locality)
        instance.city = validated_data.get("city", instance.city)
        instance.state = validated_data.get("state", instance.state)
        instance.contact_person = validated_data.get("contact_person", instance.contact_person)
        instance.contact_number = validated_data.get("contact_number", instance.contact_number)
        instance.image1 = validated_data.get("image1", instance.image1)
        instance.image2 = validated_data.get("image2", instance.image2)
        instance.image3 = validated_data.get("image3", instance.image3)
        instance.image4 = validated_data.get("image4", instance.image4)
        instance.image5 = validated_data.get("image5", instance.image5)
        instance.save()
        return instance
    
    def to_internal_value(self, data):
        if 'created_by' in data:
            data['created_by'] = None
        if 'modified_by' in data:
            data['modified_by'] = None
        return super(LocationSerializer, self).to_internal_value(data)
    

class PitchSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(required=False, queryset=Location.objects.all(), allow_null=True)
    location_data = LocationSerializer(required=False, allow_null=True)

    created_by = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all(), allow_null=True)
    created_by_data = UserSerializer(required=False, allow_null=True)

    modified_by = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all(), allow_null=True)
    modified_by_data = UserSerializer(required=False, allow_null=True)

    class Meta:
        model = Pitch
        fields = (
            "id",
            "pitch_number",
            "location",
            "location_data",
            "pitch_type",
            "starting_time",
            "ending_time",
            "break_starting_time",
            "break_ending_time",
            "status",

            #Statistics
            "created_on",
            "created_by",
            "created_by_data",
            "modified_on",
            "modified_by",
            "modified_by_data"
        )
        read_only_fields = ["id", "created_on", "created_by"]

    def create(self, validated_data):
        instance = Pitch(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.pitch_number = validated_data.get("pitch_number", instance.pitch_number)
        instance.location = validated_data.get("location", instance.location)
        instance.pitch_type = validated_data.get("pitch_type", instance.pitch_type)
        instance.starting_time = validated_data.get("starting_time", instance.starting_time)
        instance.ending_time = validated_data.get("ending_time", instance.ending_time)
        instance.break_starting_time = validated_data.get("break_starting_time", instance.break_starting_time)
        instance.break_ending_time = validated_data.get("break_ending_time", instance.break_ending_time)
        instance.status = validated_data.get("status", instance.status)
        instance.modified_on = validated_data.get("modified_on", instance.modified_on)
        instance.modified_by = validated_data.get("modified_by", instance.modified_by)
        instance.save()
        return instance

    def to_internal_value(self, data):
        if 'location_data' in data:
            data['location_data'] = None
        if 'created_by' in data:
            data['created_by'] = None
        if 'modified_by' in data:
            data['modified_by'] = None
        return super(PitchSerializer, self).to_internal_value(data)
    

class TimeSlotSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all(), allow_null=True)
    created_by_data = UserSerializer(required=False, allow_null=True)

    modified_by = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all(), allow_null=True)
    modified_by_data = UserSerializer(required=False, allow_null=True)

    class Meta:
        model = TimeSlot
        fields = (
            "id",
            "duration",
            "slot_start_time",
            "slot_end_time",
            "status",

            #Statistics
            "created_on",
            "created_by",
            "created_by_data",
            "modified_on",
            "modified_by",
            "modified_by_data"
        )
        read_only_fields = ["id", "created_on", "created_by"]

    def create(self, validated_data):
        instance = TimeSlot(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.duration = validated_data.get("duration", instance.duration)
        instance.slot_start_time = validated_data.get("slot_start_time", instance.slot_start_time)
        instance.slot_end_time = validated_data.get("slot_end_time", instance.slot_end_time)
        instance.status = validated_data.get("status", instance.status)
        instance.modified_on = validated_data.get("modified_on", instance.modified_on)
        instance.modified_by = validated_data.get("modified_by", instance.modified_by)
        instance.save()
        return instance

    def to_internal_value(self, data):
        if 'created_by' in data:
            data['created_by'] = None
        if 'modified_by' in data:
            data['modified_by'] = None
        return super(PitchSerializer, self).to_internal_value(data)
    

class CouponSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all(), allow_null=True)
    created_by_data = UserSerializer(required=False, allow_null=True)

    modified_by = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all(), allow_null=True)
    modified_by_data = UserSerializer(required=False, allow_null=True)

    class Meta:
        model = Coupon
        fields = (
            "id",
            "coupon_code",
            "validity",
            "max_users",                # Maximum Number of users that can redeem this coupon
            "max_count",                # Number of times a user can avail a coupon
            "redeem_count",             # Number of times coupon is redeemed  
            "exclusive_for",            # If coupon is exclusive for a specific user. If null then any user can redeem it if it's valid 
            "discount_type",      
            "discount_value",
            "description",
            "status",

            #Statistics
            "created_on",
            "created_by",
            "created_by_data",
            "modified_on",
            "modified_by",
            "modified_by_data"
        )
        read_only_fields = ["id", "created_on", "created_by"]

    def create(self, validated_data):
        instance = Coupon(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.coupon_code = validated_data.get("coupon_code", instance.coupon_code)
        instance.validity = validated_data.get("validity", instance.validity)
        instance.max_users = validated_data.get("max_users", instance.max_users)
        instance.max_count = validated_data.get("max_count", instance.max_count)
        instance.redeem_count = validated_data.get("redeem_count", instance.redeem_count)
        instance.exclusive_for = validated_data.get("exclusive_for", instance.exclusive_for)
        instance.discount_type = validated_data.get("discount_type", instance.discount_type)
        instance.discount_value = validated_data.get("discount_value", instance.discount_value)
        instance.description = validated_data.get("description", instance.description)
        instance.status = validated_data.get("status", instance.status)
        instance.modified_on = validated_data.get("modified_on", instance.modified_on)
        instance.modified_by = validated_data.get("modified_by", instance.modified_by)
        instance.save()
        return instance

    def to_internal_value(self, data):
        if 'created_by' in data:
            data['created_by'] = None
        if 'modified_by' in data:
            data['modified_by'] = None
        return super(CouponSerializer, self).to_internal_value(data)
    


class BookingSerializer(serializers.ModelSerializer):
    pitch = serializers.PrimaryKeyRelatedField(required=False, queryset=Pitch.objects.all(), allow_null=True)
    pitch_data = PitchSerializer(required=False, allow_null=True)

    applied_coupon = serializers.PrimaryKeyRelatedField(required=False, queryset=Coupon.objects.all(), allow_null=True)
    applied_coupon_data = CouponSerializer(required=False, allow_null=True)

    booking_for = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all(), allow_null=True)
    booking_for_data = UserSerializer(required=False, allow_null=True)

    created_by = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all(), allow_null=True)
    created_by_data = UserSerializer(required=False, allow_null=True)

    modified_by = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all(), allow_null=True)
    modified_by_data = UserSerializer(required=False, allow_null=True)

    class Meta:
        model = Booking
        fields = (
            "id",
            "booking_date",
            "pitch",
            "pitch_data",
            "time_slot",
            "total_amount",
            "applied_coupon",
            "applied_coupon_data",
            "discount",
            "net_amount",
            "paid_amount",
            "balance_amount",
            "booking_for",
            "booking_for_data",
            "payment_transactions",
            "booking_year",
            "booking_month",
            "booking_day",
            "status",

            #Statistics
            "created_on",
            "created_by",
            "created_by_data",
            "modified_on",
            "modified_by",
            "modified_by_data",
        )
        read_only_fields = ["id", "created_on", "created_by"]

    def create(self, validated_data):
        instance = Booking(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.booking_date = validated_data.get("booking_date", instance.booking_date)
        instance.pitch = validated_data.get("pitch", instance.pitch)
        instance.time_slot = validated_data.get("time_slot", instance.time_slot)
        instance.total_amount = validated_data.get("total_amount", instance.total_amount)
        instance.applied_coupon = validated_data.get("applied_coupon", instance.applied_coupon)
        instance.discount = validated_data.get("discount", instance.discount)
        instance.net_amount = validated_data.get("net_amount", instance.net_amount)
        instance.paid_amount = validated_data.get("paid_amount", instance.paid_amount)
        instance.balance_amount = validated_data.get("balance_amount", instance.balance_amount)
        instance.booking_for = validated_data.get("booking_for", instance.booking_for)
        instance.transactions = validated_data.get("transactions", instance.transactions)
        instance.modified_on = validated_data.get("modified_on", instance.modified_on)
        instance.modified_by = validated_data.get("modified_by", instance.modified_by)
        instance.save()
        return instance

    def to_internal_value(self, data):
        if 'pitch_data' in data:
            data['pitch_data'] = None
        if 'applied_coupon_data' in data:
            data['applied_coupon_data'] = None
        if 'booking_for_data' in data:
            data['booking_for_data'] = None
        if 'created_by_data' in data:
            data['created_by_data'] = None
        if 'modified_by_data' in data:
            data['modified_by_data'] = None
        return super(BookingSerializer, self).to_internal_value(data)
    

class ReservedBookingSerializer(serializers.ModelSerializer):
    pitch = serializers.PrimaryKeyRelatedField(required=False, queryset=Pitch.objects.all(), allow_null=True)
    pitch_data = PitchSerializer(required=False, allow_null=True)

    reserved_for = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all(), allow_null=True)
    reserved_for_data = UserSerializer(required=False, allow_null=True)

    created_by = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all(), allow_null=True)
    created_by_data = UserSerializer(required=False, allow_null=True)

    modified_by = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all(), allow_null=True)
    modified_by_data = UserSerializer(required=False, allow_null=True)

    class Meta:
        model = ReservedBooking
        fields = (
            "id",
            "reserved_for",
            "reserved_for_data",
            "pitch",
            "pitch_data",
            "time_slot",
            "weekdays",
            "exception_dates",

            #Statistics
            "created_on",
            "created_by",
            "created_by_data",
            "modified_on",
            "modified_by",
            "modified_by_data",
        )
        read_only_fields = ["id", "created_on", "created_by"]

    def create(self, validated_data):
        instance = ReservedBooking(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.reserved_for = validated_data.get("reserved_for", instance.reserved_for)
        instance.pitch = validated_data.get("pitch", instance.pitch)
        instance.time_slot = validated_data.get("time_slot", instance.time_slot)
        instance.weekdays = validated_data.get("weekdays", instance.weekdays)
        instance.exception_dates = validated_data.get("exception_dates", instance.exception_dates)
        instance.modified_on = validated_data.get("modified_on", instance.modified_on)
        instance.modified_by = validated_data.get("modified_by", instance.modified_by)
        instance.save()
        return instance

    def to_internal_value(self, data):
        if 'pitch_data' in data:
            data['pitch_data'] = None
        if 'reserved_for_data' in data:
            data['reserved_for_data'] = None
        if 'created_by_data' in data:
            data['created_by_data'] = None
        if 'modified_by_data' in data:
            data['modified_by_data'] = None
        return super(ReservedBookingSerializer, self).to_internal_value(data)