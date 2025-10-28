from django.forms import ModelForm
from .models import Room, User
# from  django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        #fields = ['name', 'description', 'topic', 'createdAt'] gets all specified Room attributes
        fields = '__all__' # gets all the Room the attributes
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio', 'avatar',]