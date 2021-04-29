from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import Count, Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils.models import TimeStampedModel
from phone_field import PhoneField
from rest_framework.authtoken.models import Token

from catering.models import CaterRequest
from trucks.models import Truck, Visit, Review


class MyUserManager(BaseUserManager):
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

    def create_superuser(self, email, username, password, phone=None, first_name='Super', last_name='User'):
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


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    phone = PhoneField(blank=True, null=True, default=None)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    profile_picture = models.ImageField(
        upload_to='uploads/user/profile-pictures', blank=True, default='/assets/grubtruck.png')
    biography = models.TextField(max_length=1000, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = MyUserManager()

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def my_favorite_trucks(self):
        return self.favorite_trucks.all()

    @property
    def truck_favorites(self):
        if not self.is_truck_owner:  # TODO: Is this better than nothing?
            return 0

        return Truck.objects.aggregate(count=Count('favorites', filter=Q(owner=self)))['count']

    @property
    def has_favorited_truck(self, truck):
        return TruckFavorite.objects.get(
            truck=truck,
            user=self,
        ).exists()

    @property
    def truck_views(self):
        if not self.is_truck_owner:  # TODO: Is this better than nothing?
            return 0

        return Visit.owner_visits(self)

    @property
    def my_cater_requests(self):
        return CaterRequest.objects.filter(truck__owner=self)

    @property
    def is_truck_owner(self):
        return Truck.objects.filter(owner=self).count() > 0

    @property
    def trucks(self):
        return Truck.objects.filter(owner=self).all()

    @property
    def reviews(self):
        return Review.objects.filter(reviewer=self).all()

    @property
    def cater_requests(self) -> [CaterRequest]:
        return CaterRequest.objects.filter(truck__owner=self)

    @property
    def search_history(self):
        return self.search_terms.all()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def had_module_perms(self, app_label):
        return True



class SearchTerm(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='search_terms')
    term = models.CharField(max_length=128, blank=False, null=False)
    searched_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '"{}" searched by {} on {}'.format(self.term, self.user, self.searched_on)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='feedback')
    description = models.CharField(max_length=999, blank=False, null=False)
    image = models.ImageField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)


class UserReportModel(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported')
    description = models.TextField(max_length=2048, blank=False, null=False)
