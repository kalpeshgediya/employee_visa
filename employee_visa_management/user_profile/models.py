from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)

    # Required for Django's PermissionsMixin and admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class UserData(models.Model):
    particulars = models.CharField(max_length=500)
    email = models.EmailField(null=True, blank=True)
    remarks = models.CharField(max_length=1000)
    citizen_ship = models.CharField(max_length=500)
    licence_no = models.CharField(max_length=500)
    expiry_date = models.DateTimeField()
    email_sent = models.BooleanField(default=False)