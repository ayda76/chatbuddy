from rest_framework.routers import DefaultRouter
from conversation_app.api.views import *
from django.contrib import admin
from django.urls import path , include ,re_path

router = DefaultRouter()
# router.register("", ProfileViewSet)



urlpatterns = [

    path("", include(router.urls)),
#     path('change/password/', PasswordChangeView.as_view()),

    
]