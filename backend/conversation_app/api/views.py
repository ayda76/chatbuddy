from rest_framework import generics, viewsets
from rest_framework.decorators import api_view ,permission_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from user_app.api.serializers import *
from user_app.models import Profile

from rest_framework import generics
from django.utils.decorators import method_decorator

from django.conf import settings

from django.db.models import Q

from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema 

from rest_framework.generics import ListAPIView , CreateAPIView, UpdateAPIView,DestroyAPIView

from rest_framework_simplejwt.tokens import RefreshToken
from conversation_app.models import *
from conversation_app.api.serializers import *


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    my_tags = ["Conversation"]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    my_tags = ["Conversation"]


class MessageConversation(CreateAPIView):

    serializer_class = MessageConversationSerializer
    my_tags = ["Conversation"]
    
    def post(self,request):
        profile_selected = Profile.get_user_jwt(self,self.request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            conversation_id = serializer.validated_data['conversation_id']
            conversation_selected=Conversation.objects.get(id=conversation_id)
            selected_messages=Message.objects.filter(conversationRelated=conversation_selected).order_by('created_at')
            for message in selected_messages:
                if profile_selected not in  message.read_people.all():
                    message.read_people.add(profile_selected)
                    message.save()
                    
                if profile_selected in message.fav_people.all():
                    message.is_fav=True
                    message.save()
                    
            return Response(MessageSerializer(selected_messages,many=True).data  )  
                    
class MessageFav(CreateAPIView):

    serializer_class = MessageFavSerializer
    my_tags = ["Conversation"]
    def post(self,request):
        profile_selected = Profile.get_user_jwt(self,self.request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            message_id = serializer.validated_data['message_id']
            
            mesasge_selected=Message.objects.get(id=message_id)
            
            if profile_selected in mesasge_selected.fav_people.all():
                mesasge_selected.fav_people.remove(profile_selected)
            else:
                mesasge_selected.fav_people.add(profile_selected)

            mesasge_selected.save()
            return serializer   
            