from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User
from user_app.api.serializers import ProfileSerializer

from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from conversation_app.models import * 


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'
 
class ConversationWithRelatedSerializer(serializers.ModelSerializer):
    people=serializers.SerializerMethodField() 
    class Meta:
        model = Conversation
        fields = '__all__' 
        
    def get_people(self,obj):
        peopleSelected=obj.people.all()             
        return ProfileSerializer(peopleSelected,many=True).data                      
  
      
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class MessageWithRelatedSerializer(serializers.ModelSerializer):
    
    conversation_related=ConversationSerializer(required=True)
    sender=ProfileSerializer(required=True)
    fav_people=serializers.SerializerMethodField() 
    read_people=serializers.SerializerMethodField()                        
    class Meta:
        model = Message
        fields = '__all__'
        
    def get_fav_people(self,obj):
        fav_people_selected=obj.fav_people.all()             
        return ProfileSerializer(fav_people_selected,many=True).data   
 
    def get_read_people(self,obj):
        read_people_selected=obj.read_people.all()             
        return ProfileSerializer(read_people_selected,many=True).data       
        
class MessageFavSerializer(serializers.Serializer):
    message_id = serializers.IntegerField(required=True)
                                     
class MessageConversationSerializer(serializers.Serializer):
    conversation_id = serializers.IntegerField(required=True)
