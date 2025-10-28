from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic, User, Message
from .forms import RoomForm, UserForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def login_view(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.POST.get('email')#.lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'email or password does not exist')
    
    context = { 'page': page }
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('/')

def register_view(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # dont commit until modified
            #user.username = user.username.lower() make the username lowercase
            user.save() # then save
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'An error occured during registration')
    context = { 'form': form }
    return render(request, 'base/login_register.html', context)

def home_view(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=query) | 
        Q(name__icontains=query) | 
        Q(description__icontains=query)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=query))

    context = { 'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages }
    return render(request, 'base/home.html', context)

def user_profile_view(request, pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    context = { 'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics }
    return render(request, 'base/profile.html', context)

@login_required(login_url='base:login')
def update_user_view(request):
    user = request.user
    form = UserForm(instance=request.user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('base:user-profile', pk=user.id)

    return render(request, 'base/update_user.html', { 'form': form })


def room_view(request, pk):
    room = Room.objects.get(id=pk)
    room_messages =  room.message_set.all().order_by('-createdAt') # order by recent
    # query child objects (Gives us the set of Message Data) related to the room
    # in the Message Model (Since its a foreign key)
    participants = room.participants.all()

    if request.method == 'POST':
        body = request.POST.get('body').strip()
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = body
        )
        room.participants.add(request.user)
        return redirect('base:room', pk=room.id)
    context = { 'room': room, 'room_messages': room_messages, 'participants': participants }
    return render(request, 'base/room.html', context)

@login_required(login_url='base:login')
def room_form_view(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        #request.POST.get('name') gets the name only
        topic_name = request.POST.get('topic')
        topic, createdAt = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('/')
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
            # return redirect('/')
    
    context = { 'form': form, 'topics': topics }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='base:login')
def update_room_form_view(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host and not request.user.is_superuser:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        #     return redirect('/')
    
    context = { 'form': form, 'topics': topics, 'room': room }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='base:login')
def delete_room_form_view(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
            return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('/')
    return render(request, 'base/delete.html', { 'obj': room })

@login_required(login_url='base:login')
def delete_message_form_view(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST':
        room_pk = message.room.id
        message.delete()
        return redirect('base:room', pk=room_pk)
    return render(request, 'base/delete.html', { 'obj': message })
