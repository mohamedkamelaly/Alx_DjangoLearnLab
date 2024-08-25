from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


# Create your models here.



    #USERNAME_FIELD = "email"
    #REQUIRED_FIELDS = []

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, date_of_birth=None, profile_photo=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, date_of_birth=date_of_birth, profile_photo=profile_photo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to= 'profile_photo',null=True, blank=True)
    objects = CustomUserManager()
    # Avoid clashes by specifying unique related_names
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Add a unique related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Add a unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200,null= False, default= 'Unknown title')
    author = models.CharField(max_length=100, default='Unknown Author')
    publication_year = models.IntegerField(null= False, default=timezone.now())

class CustomPermission(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    class Meta:
        permissions = [
            ('can_view', 'Can view model'),
            ('can_create', 'Can create model'),
            ('can_edit', 'Can edit model'),
            ('can_delete', 'Can delete model'),
        ]