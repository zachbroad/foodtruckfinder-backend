from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from phone_field import PhoneField
from rest_framework.authtoken.models import Token
from trucks.models import Truck

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, phone='555-555-5555', first_name='Super', last_name='User'):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = PhoneField(default='555-555-5555')
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    @property
    def favorites(self):
        return self.favorite_trucks.all()

    @property
    def search_history(self):
        return self.search_terms.all()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def had_module_perms(self, app_label):
        return True


class FavoriteTruck(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_trucks')
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, )
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'truck')

    def __str__(self):
        return '{} favorited by {}'.format(self.truck.title, self.user.username)

    @staticmethod
    def pre_save(instance, sender, **kwargs):
        instance.truck = Truck.objects.get(user__id=instance.user, truck__id=instance.truck.pk)
        print(instance)


pre_save.connect(FavoriteTruck.pre_save, FavoriteTruck, dispatch_uid="sightera.yourpackage.models.TodoList")


class SearchTerm(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='search_terms')
    term = models.CharField(max_length=50, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
