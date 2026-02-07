from rest_framework.routers import DefaultRouter
from conversation_app.api.views import *
from django.contrib import admin
from django.urls import path , include ,re_path

router = DefaultRouter()

router.register("", ConversationViewSet)
router.register("message", MessageViewSet)



urlpatterns = [

    path("", include(router.urls)),
    path('messagesConversation', MessageConversation.as_view()),
    path('favoriteMessages', MessageFav.as_view()),

    
]