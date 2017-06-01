from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.text import slugify
from rest_framework.authtoken.models import Token

from timezone_field import TimeZoneField


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")

        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        Token.objects.create(user=user)
        return user

    def create_superuser(self, email, password):

        if not (email or password):
            raise ValueError("Super user must have an email and password")
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_staff = True
        user.save()


class User(AbstractBaseUser):
    """this class represents the user Model.
    """

    def get_short_name(self):
        pass

    def get_full_name(self):
        pass

    class Meta:
        db_table = 'users'
        managed = True

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    country_code = models.IntegerField(blank=True, null=True)
    contact_no = models.BigIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_password_changed = models.BooleanField(default=False)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    is_staff = models.IntegerField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __unicode__(self):
        return self.email


class UserResetPassword(models.Model):
    class Meta:
        db_table = 'user_reset_password'

    users = models.OneToOneField(User)
    is_valid_key = models.BooleanField(default=False)
    key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField()

    def __unicode__(self):
        return self.email


class Category(models.Model):

    class Meta:
        db_table = 'category'
        managed = True

    category_name = models.CharField(max_length=100, db_index=True)
    category_slug = models.SlugField()


def image_upload_to(instance, filename):
    title = instance.product.product_title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)

    # return something
    pass


class Product(models.Model):

    class Meta:
        db_table = 'product'
        managed = True

    product_name = models.CharField(max_length=200, db_index=True, unique=True)
    category = models.ForeignKey(Category)
    product_price = models.IntegerField()
    product_description = models.TextField(max_length=200)
    is_available = models.BooleanField(default=True)

    def __unicode__(self):
        return self.product_name


class ProductImage(models.Model):

    class Meta:
        db_table = 'product_image'
        managed = True

    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to)


class Appointment(models.Model):
    # Creates an appointment table which must be further used to send text reminders using twilio

    appointment_name = models.CharField(max_length=150)
    time = models.DateTimeField()
    time_zone = TimeZoneField(default='Asia/Kolkata')  # Indian Time Zone.

    # Adsditional fields not visible to users
    created = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def __unicode__(self):
        return self.appointment_name


class Service(models.Model):

    class Meta:
        db_table = 'services'
        managed = True

    service_name = models.CharField(max_length=100, db_index=True)
    service_category = models.ForeignKey(Category)
    service_description = models.TextField(max_length=500)
    service_appointment = models.ForeignKey(Appointment)

    def __unicode__(self):
        return self.service_name
