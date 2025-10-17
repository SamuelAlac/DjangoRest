from django.shortcuts import render
from .models import Room

# Create your views here.
def home_view(request):
    rooms = Room.objects.all()
    context = { 'rooms': rooms }
    return render(request, 'base/home.html', context)

def room_view(request, pk):
    room = Room.objects.get(id=pk)
    context = { 'room': room }
    return render(request, 'base/room.html', context)