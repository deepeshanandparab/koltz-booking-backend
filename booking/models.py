import uuid
from django.db import models
from account.models import User
import datetime
import json


def location_image_one_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/location/location_<id>/image/1/<filename>
    return 'location/{0}/image/1/{1}'.format(instance.pk, filename)

def location_image_two_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/location/location_<id>/image/2/<filename>
    return 'location/{0}/image/2/{1}'.format(instance.pk, filename)

def location_image_three_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/location/location_<id>/image/3/<filename>
    return 'location/{0}/image/3/{1}'.format(instance.pk, filename)

def location_image_four_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/location/location_<id>/image/4/<filename>
    return 'location/{0}/image/4/{1}'.format(instance.pk, filename)

def location_image_five_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/location/location_<id>/image/5/<filename>
    return 'location/{0}/image/5/{1}'.format(instance.pk, filename)

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.IntegerField(default=0, null=True, blank=True)
    image_1 = models.ImageField(upload_to=location_image_one_directory_path, height_field=None, width_field=None, max_length=100, null=True, blank=True)
    image_2 = models.ImageField(upload_to=location_image_two_directory_path, height_field=None, width_field=None, max_length=100, null=True, blank=True)
    image_3 = models.ImageField(upload_to=location_image_three_directory_path, height_field=None, width_field=None, max_length=100, null=True, blank=True)
    image_4 = models.ImageField(upload_to=location_image_four_directory_path, height_field=None, width_field=None, max_length=100, null=True, blank=True)
    image_5 = models.ImageField(upload_to=location_image_five_directory_path, height_field=None, width_field=None, max_length=100, null=True, blank=True)

    #Statistics
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="location_created_by")
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="location_modified_by")

    def __str__(self):
        return f"{self.name} - {self.locality} {self.contact_person}"  
    

class Pitch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pitch_number = models.IntegerField(default=1)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="pitch_location")

    class PitchType(models.TextChoices):
        NATURAL_TURF = "NATURAL_TURF"
        ARTIFICIAL_TURF = "ARTIFICIAL_TURF"
 
    pitch_type = models.CharField(choices=PitchType.choices, default=PitchType.NATURAL_TURF, max_length=255)
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    break_starting_time = models.TimeField(null=True, blank=True)
    break_ending_time = models.TimeField(null=True, blank=True)

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"
 
    status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=255)

    #Statistics
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="pitch_created_by")
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="pitch_modified_by")

    def __str__(self):
        return f"Pitch - {self.pitch_number} - {self.location.name} ({self.pitch_type})"
    
    def location_data(self):
        return self.location
    
    def created_by_data(self):
        return self.created_by
    
    def modified_by_data(self):
        return self.modified_by
    

class TimeSlot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    duration = models.IntegerField(default=30)
    slot_start_time = models.TimeField()
    slot_end_time = models.TimeField(null=True, blank=True)

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"
        BOOKED = "BOOKED"
 
    status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=255)

    #Statistics
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="timeslot_created_by")
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="timeslot_modified_by")

    def __str__(self):
        return f"{self.slot_start_time} - {self.slot_end_time}"
    
    def save(self, *args, **kwargs):
        self.slot_end_time = (datetime.datetime.combine(datetime.date(1,1,1), self.slot_start_time) + datetime.timedelta(minutes=self.duration)).time()
        super(TimeSlot, self).save(*args, **kwargs)

    def created_by_data(self):
        return self.created_by
    
    def modified_by_data(self):
        return self.modified_by


class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon_code = models.CharField(max_length=255, unique=True)
    validity = models.DateTimeField(null=True, blank=True)
    max_users = models.IntegerField(default=1)
    max_count = models.IntegerField(default=1)
    redeem_count = models.IntegerField(default=0)
    exclusive_for = models.ManyToManyField(User, null=True, blank=True)

    class Discount_Type(models.TextChoices):
        AMOUNT = "AMOUNT"
        PERCENTAGE = "PERCENTAGE"

    discount_type = models.CharField(choices=Discount_Type.choices, default=Discount_Type.AMOUNT, max_length=255)
    discount_value = models.FloatField(default=0.0)
    description = models.TextField(null=True, blank=True)

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"
        REDEEMED = "REDEEMED"
        EXPIRED = "EXPIRED"

    status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=255)

    #Statistics
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="coupon_created_by")
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="coupon_modified_by")

    def __str__(self):
        if self.discount_type == "AMOUNT":
            return f"{self.coupon_code} - Discount Rs. {self.discount_value}"
        else:
            return f"{self.coupon_code} - Discount {self.discount_value}%"
        
    def created_by_data(self):
        return self.created_by
    
    def modified_by_data(self):
        return self.modified_by




class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking_date = models.DateField()
    pitch = models.ForeignKey(Pitch, on_delete=models.SET_NULL, null=True, blank=True, related_name="booking_pitch")
    time_slot = models.ManyToManyField(TimeSlot)
    total_amount = models.FloatField(default=0.0)
    applied_coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name="booking_coupon")
    discount = models.FloatField(default=0.0)
    net_amount = models.FloatField(default=0.0)
    paid_amount = models.FloatField(default=0.0)
    balance_amount = models.FloatField(default=0.0)
    booking_for = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="booking_by_user")
    transactions = models.JSONField(null=True, blank=True)

    class Status(models.TextChoices):
        BOOKED = "BOOKED"
        CANCELLED = "CANCELLED"
        CONFIRMED = "CONFIRMED"
        RESERVED = "RESERVED"

    status = models.CharField(choices=Status.choices, default=Status.BOOKED, max_length=255)
    
    #Statistics
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="booking_created_by")
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="booking_modified_by")

    def __str__(self):
        return f"{self.booking_date} - {self.pitch} {self.booking_for}"
    
    def pitch_data(self):
        return self.pitch
    
    def applied_coupon_data(self):
        return self.applied_coupon
    
    def booking_for_data(self):
        return self.booking_for
    
    def created_by_data(self):
        return self.created_by
    
    def modified_by_data(self):
        return self.modified_by
    
    def payment_transactions(self):
        if self.transactions:
            transaction_data = json.dumps(self.transactions)
            print(transaction_data)
            return transaction_data
        else:
            return ""
        
    def booking_year(self):
        return self.booking_date.year
    
    def booking_month(self):
        return self.booking_date.month
    
    def booking_day(self):
        return self.booking_date.strftime("%Y-%m-%d")



class ReservedBooking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reserved_for = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reserved_booking_by_user")
    pitch = models.ForeignKey(Pitch, on_delete=models.SET_NULL, null=True, blank=True, related_name="reserved_booking_pitch")
    time_slot = models.ManyToManyField(TimeSlot)
    weekdays = models.JSONField(null=True, blank=True)
    exception_dates = models.JSONField(null=True, blank=True)

    #Statistics
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reserved_booking_created_by")
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reserved_booking_modified_by")

    def __str__(self):
        return f"{self.reserved_for.username}"
    









