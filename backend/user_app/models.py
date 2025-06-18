from django.db import models
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
import jwt


class Profile(models.Model):     
    GENDER_SELECT = (('men' , 'men') ,('women' , 'women')  )
    user       = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile" )
    firstName  = models.CharField(max_length=50 ,blank=True , null=True )
    lastName   = models.CharField(max_length=50 ,blank=True , null=True ) 
    avatar     = models.ImageField(upload_to="avatars",blank=True , null=True)
    class Meta:
        verbose_name = "اطلاعات شخصی"
        verbose_name_plural = "اطلاعات شخصی"
    def __str__(self):
        return str(self.firstName) + " " + str(self.lastName)
