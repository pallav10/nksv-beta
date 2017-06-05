from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from timezone_field import TimeZoneField


# Create your models here.

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None):
#         if not email:
#             raise ValueError("User must have an email")
#
#         user = self.model(email=email)
#         user.set_password(password)
#         user.save(using=self._db)
#         Token.objects.create(user=user)
#         return user
#
#     def create_superuser(self, email, password):
#
#         if not (email or password):
#             raise ValueError("Super user must have an email and password")
#         user = self.create_user(email, password)
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save()


class User(AbstractBaseUser, PermissionsMixin):
    """this class represents the user Model.
    """
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
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselected this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    #
    # def get_absolute_url(self):
    #     return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

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


# def image_upload_to(instance, filename):
#     title = instance.product.product_title
#     slug = slugify(title)
#     basename, file_extension = filename.split(".")
#     new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
#
#     # return something
#     pass


class Product(models.Model):
    class Meta:
        db_table = 'product'
        managed = True

    product_name = models.CharField(max_length=200, db_index=True, unique=True)
    product_category = models.ForeignKey(Category)
    product_price = models.IntegerField()
    product_description = models.TextField(max_length=200)
    product_image = models.ImageField(blank=True)
    is_available = models.BooleanField(default=True)

    def __unicode__(self):
        return self.product_name


class Appointment(models.Model):
    # Creates an appointment table which must be further used to send text reminders using twilio

    appointment_name = models.CharField(max_length=150)
    time = models.DateTimeField()
    time_zone = TimeZoneField(default='Asia/Kolkata')  # Indian Time Zone.

    # Additional fields not visible to users
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


class Blog(models.Model):
    class Meta:
        db_table = 'blog'
        managed = True

    blog_name = models.CharField(max_length=100, db_index=True)
    blog_description = models.TextField(max_length=500)
    blog_image = models.ImageField(blank=True)

    def __unicode__(self):
        return self.blog_name




