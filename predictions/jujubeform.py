from django.forms import ModelForm
from .models import JujubeImage
from django import forms  
  
  
class JujubeForm(ModelForm):  
    class Meta:  
        # To specify the model to be used to create form  
        model = JujubeImage
        # It includes all the fields of model  
        fields = ["jujube_image"]