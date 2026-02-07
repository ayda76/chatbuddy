from django.contrib import admin

from .resources import *
from import_export.admin import ImportExportModelAdmin 
# Register your models here.
from .models import *

@admin.register(Profile)
class ColorHexAdmin(ImportExportModelAdmin):

    list_display = ('id', )
    list_filter = ('id' , )
      
    search_fields = ('id' ,)
    resource_class = ProfileResource