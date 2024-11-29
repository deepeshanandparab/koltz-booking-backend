import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import FileExtensionValidator

class UserManager(BaseUserManager):
    def create_user(self, username, name=None):
        if not username:
            raise ValueError("User must have username")
        if name is not None:
            user = self.model(
                username=username,
                name=name
            )
        else:
            user = self.model(
                username=username,
            )
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, password):
        user = self.create_user(
            username,
            name
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_role_user(self, username=None, password=None, role=None, name=None, email=None, mobile=None):
        user = self.create_user(
            username,
            name
        )
        if password is None:
            password = User.objects.make_random_password()
        user.set_password(password)

        user.role_id = role
        if email is not None:
            user.email = email
        if mobile is not None:
            user.mobile = mobile
        user.save(using=self._db)
        return user



class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=255, null=True, blank=True)

    class RoleCategory(models.TextChoices):
        GUEST = "GUEST"
        PLAYER = "PLAYER"
        STAFF = "STAFF"
        ADMIN = "ADMIN"
        ACADEMY = "ACADEMY"
        SUPERADMIN = "SUPERADMIN"

    role = models.CharField(choices=RoleCategory.choices, default=RoleCategory.GUEST, max_length=255)
    role_name = models.CharField(max_length=255, null=True, blank=True)

    class RoleStatus(models.TextChoices):
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"

    status = models.CharField(choices=RoleStatus.choices, default=RoleStatus.ACTIVE, max_length=255)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role


def profile_picture_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'users/{0}/profile/{1}'.format(instance.pk, filename)

def age_proof_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'users/{0}/age_proof/{1}'.format(instance.pk, filename)

def address_proof_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'users/{0}/address_proof/{1}'.format(instance.pk, filename)



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, verbose_name="Email", null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Name")
    first_name = models.CharField(max_length=255, null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.IntegerField(default=0)

    class Gender(models.TextChoices):
        MALE = "MALE"
        FEMALE = "FEMALE"
        OTHER = "OTHER"

    gender = models.CharField(choices=Gender.choices, default=Gender.MALE, max_length=255)

    picture = models.ImageField(upload_to=profile_picture_directory_path, 
                                height_field=None, 
                                width_field=None, 
                                max_length=100, 
                                null=True, 
                                blank=True,
                                validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
                                )
    
    age_proof_document_type = models.CharField(max_length=255, null=True, blank=True)
    age_proof_document = models.ImageField(upload_to=age_proof_directory_path, height_field=None, width_field=None, max_length=100, null=True, blank=True)

    address_proof_document_type = models.CharField(max_length=255, null=True, blank=True)
    address_proof_document = models.ImageField(upload_to=address_proof_directory_path, height_field=None, width_field=None, max_length=100, null=True, blank=True)

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"

    status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=255)
    
    # Statistics
    created_on = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email', 'mobile']

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_staff
    
    @property
    def role_data(self):
        return self.role