from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        #fields = ['name', 'description', 'topic', 'createdAt'] gets all specified Room attributes
        fields = '__all__' # gets all the Room the attributes
        exclude = ['host', 'participants']