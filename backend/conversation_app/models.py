from django.db import models
from django.conf import settings
from user_app.models import Profile

class Conversation(models.Model):     

    people     = models.ManyToManyField(Profile,blank=True,related_name="conversation_people" )
    name       = models.CharField(max_length=50 ,blank=True , null=True )
    avatar     = models.ImageField(upload_to="avatars",blank=True , null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversation"
    

class Message(models.Model):     
  
    conversation_related   = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="message_conversation" )
    sender                 = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name="message_sender" )
    text_message           = models.TextField(blank=True , null=True ) 
    replied_message        = models.ForeignKey('self',on_delete=models.CASCADE, related_name="message_replied" , blank=True , null=True)
    fav_people             = models.ManyToManyField(Profile,blank=True ,related_name="fav_people_message")
    read_people            = models.ManyToManyField(Profile,blank=True ,related_name="read_people_message")
    is_fav                 = models.BooleanField(default=False, blank=True , null=True)
    created_at             = models.DateTimeField(auto_now_add=True)
    updated_at             = models.DateTimeField(auto_now=True) 
    
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Message"
        

