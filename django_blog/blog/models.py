from typing import Any
from django.conf import settings
from django.db import models
from django.contrib.auth.models import  AbstractUser, AbstractBaseUser, UserManager
from django.utils import timezone
# Create your models here.
class User_Manager(UserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Email Address must be Entered')
        if not username:
            raise ValueError('Please enter valid user name')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using= self._db)
        return user
    
    def create_superuser(self,username, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,  
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class MyUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    objects = User_Manager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date =  models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated_date = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    



#In your blog app, create a Comment model with the following fields:
#post: a ForeignKey linking to the Post model, establishing a many-to-one relationship.
#author: a ForeignKey to Django’s User model, indicating the user who wrote the comment.
#content: a TextField for the comment’s text.
#created_at: a DateTimeField that records the time the comment was made.
#updated_at: a DateTimeField that records the last time the comment was updated.
#Ensure you run migrations to create this model in the database.

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'