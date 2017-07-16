from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# from timezone_field import TimeZoneField


# Create your models here.


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

    user = models.OneToOneField(User)
    is_valid_key = models.BooleanField(default=False)
    key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField()

    def __unicode__(self):
        return self.user

    def __repr__(self):
        return str(self.id)


# class ProductCategory(models.Model):
#     class Meta:
#         db_table = 'product_categories'
#         managed = True
#
#     name = models.CharField(max_length=100, db_index=True)
#     description = models.CharField(max_length=500, blank=True)
#     image = models.ImageField(blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#     is_available = models.BooleanField(default=True)
#     is_deleted = models.BooleanField(default=False)
#     # slug = models.SlugField()
#
#     def __unicode__(self):
#         return self.name
#
#
# class Product(models.Model):
#     class Meta:
#         db_table = 'products'
#         managed = True
#
#     product_category = models.ForeignKey(ProductCategory)
#     name = models.CharField(max_length=200, db_index=True, unique=True)
#     description = models.TextField(max_length=200)
#     price = models.IntegerField()
#     image = models.ImageField(blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#     is_available = models.BooleanField(default=True)
#     is_deleted = models.BooleanField(default=False)
#
#     def __unicode__(self):
#         return self.name
#
#     def __repr__(self):
#         return str(self.id)
#
#
# class ServiceCategory(models.Model):
#     class Meta:
#         db_table = 'service_categories'
#         managed = True
#
#     name = models.CharField(max_length=100, db_index=True)
#     description = models.CharField(max_length=500, blank=True)
#     image = models.ImageField(blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#     is_available = models.BooleanField(default=True)
#     is_deleted = models.BooleanField(default=False)
#
#     # slug = models.SlugField()
#
#     def __unicode__(self):
#         return self.name
#
#     def __repr__(self):
#         return str(self.id)
#
#
# class Service(models.Model):
#     class Meta:
#         db_table = 'services'
#         managed = True
#
#     service_category = models.ForeignKey(ServiceCategory)
#     name = models.CharField(max_length=200, db_index=True, unique=True)
#     description = models.TextField(max_length=200)
#     price = models.IntegerField()
#     image = models.ImageField(blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#     is_available = models.BooleanField(default=True)
#     is_deleted = models.BooleanField(default=False)
#
#     def __unicode__(self):
#         return self.name
#
#     def __repr__(self):
#         return str(self.id)

#
# class Order(models.Model):
#     class Meta:
#         db_table = 'orders'
#         managed = True
#
#     user = models.ForeignKey(User)
#     name = models.CharField(max_length=200, blank=True)
#     description = models.CharField(max_length=500, blank=True)
#     paid_date = models.DateTimeField(auto_now_add=True)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#     notes = models.CharField(max_length=400, blank=True)
#
#     def __unicode__(self):
#         return self.name
#
#     def __repr__(self):
#         return str(self.id)
#
#
# class OrderProduct(models.Model):
#     class Meta:
#         db_table = 'order_products'
#         managed = True
#
#     order = models.ForeignKey(Order)
#     product_category = models.ForeignKey(ProductCategory)
#     product = models.ForeignKey(Product)
#     quantity = models.IntegerField(default=1)
#
#     def __unicode__(self):
#         return self.id
#
#     def __repr__(self):
#         return str(self.id)
#
#
# class OrderService(models.Model):
#     class Meta:
#         db_table = 'order_services'
#         managed = True
#
#     order = models.ForeignKey(Order)
#     service_category = models.ForeignKey(ServiceCategory)
#     service = models.ForeignKey(Service)
#     quantity = models.IntegerField(default=1)
#
#     def __unicode__(self):
#         return self.id
#
#     def __repr__(self):
#         return str(self.id)


class ItemType(models.Model):
    class Meta:
        db_table = 'item_type'
        managed = True

    TYPE_CHOICES = [('product', 'product'), ('service', 'service')]
    name = models.CharField(max_length=20, choices=TYPE_CHOICES, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    class Meta:
        db_table = 'categories'
        managed = True

    item_type = models.ForeignKey(ItemType)
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return str(self.id)


class Item(models.Model):
    class Meta:
        db_table = 'items'
        managed = True

    category = models.ForeignKey(Category)
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(blank=True)
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return str(self.id)


class Cart(models.Model):
    class Meta:
        db_table = 'cart'
        managed = True
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()

    def __unicode__(self):
        return self.id

    def __repr__(self):
        return str(self.id)


# def image_upload_to(instance, filename):
#     title = instance.product.product_title
#     slug = slugify(title)
#     basename, file_extension = filename.split(".")
#     new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
#
#     # return something
#     pass


# class Appointment(models.Model):
#     # Creates an appointment table which must be further used to send text reminders using twilio
#
#     appointment_name = models.CharField(max_length=150)
#     time = models.DateTimeField()
#     time_zone = TimeZoneField(default='Asia/Kolkata')  # Indian Time Zone.
#
#     # Additional fields not visible to users
#     created = models.DateTimeField(auto_now_add=True)
#     is_available = models.BooleanField(default=True)
#
#     def __unicode__(self):
#         return self.appointment_name

class Article(models.Model):
    class Meta:
        db_table = 'articles'
        managed = True

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return str(self.id)


class ImageGallery(models.Model):
    class Meta:
        db_table = 'images'
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=400, blank=True)
    image = models.ImageField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return str(self.id)


class VideoGallery(models.Model):
    class Meta:
        db_table = 'videos'
        managed = True

    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=400, blank=True)
    video = models.FileField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return str(self.id)


class Horoscope(models.Model):
    class Meta:
        db_table = 'horoscopes'
        managed = True

    CATEGORY_CHOICES = [('daily', 'daily'), ('weekly', 'weekly'), ('yearly', 'yearly')]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=False, default='daily')
    HOROSCOPE_CHOICES = [('Aries', 'Aries'), ('Taurus', 'Taurus'), ('Gemini', 'Gemini'), ('Cancer', 'Cancer'),
                         ('Leo', 'Leo'), ('Virgo', 'Virgo'), ('Libra', 'Libra'), ('Scorpio', 'Scorpio'),
                         ('Sagittarius', 'Sagittarius'), ('Capricorn', 'Capricorn'), ('Aquarius', 'Aquarius'),
                         ('Pisces', 'Pisces')]
    name = models.CharField(max_length=20, choices=HOROSCOPE_CHOICES, blank=False, default='Aries')
    description = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return str(self.id)

# class ChildNameClients(models.Model):
#     class Meta:
#         db_table = 'child_name_clients'
#         managed = True
#
#     GENDER_CHOICES = [('son', 'son'), ('daughter', 'daughter')]
#     gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=False, default='son')
#     client_email = models.EmailField(max_length=254, unique=True)
#     client_contact_no = models.BigIntegerField(blank=True, null=True)
#     date = models.DateField(blank=True, null=True)


