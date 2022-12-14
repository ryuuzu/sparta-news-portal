from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import models
from django.contrib.auth.hashers import make_password
from django.db import models
from slugify import slugify

# Local Imports
from .choices import UserTypes

# from .models import AppUser


class PortalUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username or len(username) <= 0:
            raise ValueError("Manager: Username cannot be empty!!!")
        if not password:
            raise ValueError("Manager: Password cannot be null!!!")
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save(using=self._db)

        return user


class ReporterManager(models.Manager):
    def create_user(self, username, password):
        if not username or len(username) <= 0:
            raise ValueError("Manager:  Username cannot be empty!!!")
        if not password:
            raise ValueError("Manager: Password cannot be null!!!")

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create(self, **kwargs):
        password = kwargs["password"]
        kwargs["password"] = make_password(password)
        return super().create(**kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        result = queryset.filter(user_type=UserTypes.REPORTER)
        return result


class NewsManager(models.Manager):
    def create(self, **kwargs):
        slug = slugify(kwargs["title"])
        return super().create(slug=slug, **kwargs)


class ReaderManager(models.Manager):
    def create_user(self, username, password):
        if not username or len(username) <= 0:
            raise ValueError("Manager:  Username cannot be empty!!!")
        if not password:
            raise ValueError("Manager: Password cannot be null!!!")

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self):
        queryset = super().get_queryset()
        result = queryset.filter(user_type=UserTypes.READER)
        return result
