from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from rest_framework.authtoken.models import Token


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
    is_active = models.IntegerField(default=False)

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

