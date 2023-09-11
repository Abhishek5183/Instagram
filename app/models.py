from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UserProfileManager( BaseUserManager):
    def create_user(self, username, email, phone_number,password = None):
        if not email:
            raise ValueError('Email not provided')
        New_email = self.normalize_email(email)
        UPO = self.model(email = email, username = username, phone_number = phone_number)
        UPO.set_password(password)
        UPO.save()
        return UPO
    def create_superuser(self,username, email, phone_number, password):
        UPO = self.create_user(username, email, phone_number,password)
        UPO.is_staff = True
        UPO.is_superuser = True
        UPO.save()

class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    email = models.EmailField(primary_key= True)
    phone_number = models.CharField(max_length=12)
    password = models.CharField(max_length=100)
    id = models.CharField(max_length=10,default= 1)
    image = models.ImageField(blank= True, upload_to= 'media')
    gender = models.CharField(default= 'nil', max_length= 100)
    bio = models.CharField(default='I am no one to harm you. I’ll let karma bash you.', max_length=100)
    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default= False)
    is_superuser = models.BooleanField(default= False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number','password']


class Uploaded_images(models.Model):
    user_id = models.EmailField(max_length=100, blank=True)
    image = models.ImageField(upload_to= 'media', blank=True)

class Followers(models.Model):
    email = models.ForeignKey(UserProfile,to_field='email', on_delete= models.CASCADE)
    follower_id = models.EmailField(max_length=100)
    active = models.IntegerField(default= 0)