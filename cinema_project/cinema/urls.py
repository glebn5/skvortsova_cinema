from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('seans/<int:seans_id>/', views.seans_detail, name='seans_detail'),
    path('seans/<int:seans_id>/book/<int:seat_id>/', views.book_seat, name='book_seat'),
    path('register/', views.register, name='register'),


]
