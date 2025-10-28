from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_view, name='register'),
    path('', views.home_view, name='home'),
    path('user-profile/<str:pk>/', views.user_profile_view, name='user-profile'),
    path('create-room/', views.room_form_view, name='create-room'),
    path('room/<str:pk>/', views.room_view, name='room'),
    path('update-room/<str:pk>/', views.update_room_form_view, name='update-room'),
    path('delete-room/<str:pk>/', views.delete_room_form_view, name='delete-room'),
    path('delete-message/<str:pk>/', views.delete_message_form_view, name='delete-message'),
    path('update-user/', views.update_user_view, name='update-user')
]