# from django.db import models
# import uuid
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.utils.translation import gettext_lazy as _
# import datetime
#
#
# # Create your models here.
#
# class UserManager(BaseUserManager):
#
#     use_in_migrations = True
#
#     def create_user(self, email, name, date_of_birth, password, **kwargs):
#         email = self.normalize_email(email)
#
#         new_user = self.model(
#             name=name,
#             email=email,
#             date_of_birth=date_of_birth,
#             is_active=True,
#             **kwargs
#         )
#
#         new_user.set_password(password)
#         new_user.save(using=self._db)
#
#         return new_user
#
#     def create_superuser(self, email, name, date_of_birth, password):
#         new_spuser = self.create_user(
#             name=name,
#             email=email,
#             date_of_birth=date_of_birth,
#             password=password,
#             is_admin=True,
#         )
#
#         return new_spuser
#
#
# class User(AbstractBaseUser):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(_('Name'), max_length=255)
#     email = models.EmailField(_('Email'), max_length=255, unique=True)
#     date_of_birth = models.DateField(_('Birthdate'), default=datetime.date.today)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name', 'date_of_birth']
#
#     objects = UserManager()
#
#     class Meta:
#         app_label = 'accounts'
#         verbose_name = _('User')
#         verbose_name_plural = _('Users')
#         # db_table = 'accounts_user'
#
#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         return self.is_admin
#
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     def __str__(self):
#         return self.email

import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    birthday = models.DateField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return self.get_full_name()
