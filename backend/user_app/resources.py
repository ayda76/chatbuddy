from import_export import resources
from .models import *

class ProfileResource(resources.ModelResource):
     class Meta:
          model = Profile