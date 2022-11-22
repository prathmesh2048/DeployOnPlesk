from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from helper import helper
import uuid


class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password, referee=None):
        user = self.model(username=username, email=email)

        try:
            referral_code = helper.generateCode(8)
        except Exception:
            referral_code = helper.generateCode(8)

        if referee:
            user.referee = referee
        else:
            user.referee = None

        user.set_password(password)
        user.is_verified = False
        user.is_2fa = False
        user.is_active = True
        user.referral_code = referral_code
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username, email=email, password=password)
        user.is_superuser = True
        user.is_verified = True
        user.is_2fa = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    # Required fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        max_length=50, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)

    # permissions and varification fields
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # login data fields
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # packetstream data
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    objects = MyAccountManager()

    def __str__(self):
        return self.id

    class Meta:
        db_table = "users"
