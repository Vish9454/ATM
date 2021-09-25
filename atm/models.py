from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (AbstractBaseUser, UserManager)
from django.contrib.postgres.fields import ArrayField
from django.contrib.gis.db import models
# Create your models here.

class BaseModel(models.Model):
    """
    Base models to save the common properties such as:
        created_at, updated_at, is_deleted.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated At')
    is_deleted = models.BooleanField('Is Deleted', default=False)

    class Meta:
        abstract = True
        verbose_name = 'BaseModel'
        index_together = ["created_at", "updated_at"]


class MyUserManager(BaseUserManager):
    """
    Inherits: BaseUserManager class
    """

    def create_user(self, email, password=None):
        """
        Create user with given email and password.
        :param email:
        :param password:
        :return:
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        # set_password is used set password in encrypted form.
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and save the super user with given email and password.
        :param email:
        :param password:
        :return: user
        """
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.username = ""
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class ActiveUserManager(UserManager):
    """
        ActiveUserManager class to filter the deleted user.
    """

    def get_queryset(self):
        return super(ActiveUserManager, self).get_queryset().filter(is_active=True, is_deleted=False)


class ActiveObjectsManager(UserManager):
    """
        ActiveObjectsManager class to filter the deleted objs
    """

    def get_queryset(self):
        return super(ActiveObjectsManager, self).get_queryset().filter(is_deleted=False)


class User(AbstractBaseUser, BaseModel):
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Last Name')
    full_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Full Name')
    email = models.EmailField(max_length=80, unique=True, blank=False, null=False, verbose_name='Email')
    is_active = models.BooleanField('Active', default=True)
    is_staff = models.BooleanField('Is Staff', default=False)
    is_superuser = models.BooleanField('SuperUser', default=False)

    objects = ActiveUserManager()
    all_objects = ActiveObjectsManager()
    all_delete_objects = UserManager()
    my_user_manager = MyUserManager()
    USERNAME_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        """
        :return: email
        """
        return self.email

    def get_short_name(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        ordering = ['id']


class ATMDetails(BaseModel):
    street = models.CharField(max_length=50, blank=True, null=True, verbose_name='street')
    housenumber = models.CharField(max_length=50, blank=True, null=True, verbose_name='house number')
    postalcode = models.CharField(max_length=50, blank=True, null=True, verbose_name='postal code')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='city')
    geolocation = models.PointField(blank=True, null=True, verbose_name='geo location')
    distance = models.FloatField(blank=True, null= True)
    openingHours = models.JSONField(blank=True, null=True)
    functionality = models.CharField(max_length=50, blank=True, null=True, verbose_name='funtionality')
    type = models.CharField(max_length=50, blank=True, null=True, verbose_name='type of ATM')
    address = models.JSONField(blank=True, null=True)