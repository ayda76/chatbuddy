from django.db import models
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
import jwt


class Profile(models.Model):     
    user       = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile" )
    firstName  = models.CharField(max_length=50 ,blank=True , null=True )
    lastName   = models.CharField(max_length=50 ,blank=True , null=True ) 
    avatar     = models.ImageField(upload_to="avatars",blank=True , null=True)
    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profile"
    def __str__(self):
        return str(self.firstName) + " " + str(self.lastName)
    
    def get_user_jwt(self,request):
        token = get_authorization_header(request).decode('utf-8')
        if token is None or token == "null" or token.strip() == "":
            raise exceptions.AuthenticationFailed('Authorization Header or Token is missing on Request Headers')
        
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        
        username = decoded['user_id']
        return Profile.objects.get(user__id=username)
