from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('movie/<str:pk>/', views.movie, name='movie'), #to view the selected movie details
    path('add-to-list', views.add_to_list, name='add-to-list'),
    path('my-list', views.my_list, name='my-list'),
    path('search', views.search, name='search'),
    path('genre/<str:pk>/', views.genre, name='genre'),
]