from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
import uuid
from portals.choices import UserChoices
# Create your models here.

import os 
class User(AbstractBaseUser):
    id         = models.UUIDField(default=uuid.uuid4,primary_key=True)
    email      = models.EmailField(
        verbose_name='email address',
        max_length=255,
        null=True,
        blank=True
    )
    is_admin         = models.BooleanField(default=False)
    username         = models.CharField(max_length = 50)
    profile_pic      = models.ImageField(upload_to="user/",null=True,blank=True)
    mobile_number    = models.CharField(max_length=20,unique=True)
    user_role        = models.CharField(choices=UserChoices.choices,max_length=50,default=UserChoices.CUSTOMER)
    accepted_policy  = models.BooleanField(default=False)
    objects          = UserManager()
    email_otp        = models.CharField(max_length=6,blank=True,null=True)
    sms_otp          = models.CharField(max_length=6,blank=True,null=True)
    is_verified      = models.BooleanField(default=False)
    
    user_role        = models.CharField
    
    created_on       = models.DateTimeField(auto_now_add=True,editable=False)
    updated_on       = models.DateTimeField(auto_now=True)
   
    
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    def __str__(self) -> str:
        return self.username

    
    def delete(self, *args, **kwargs):
        if self.profile_pic:
            if os.path.isfile(self.profile_pic.path):
                os.remove(self.profile_pic.path)
        super(User, self).delete(*args, **kwargs)