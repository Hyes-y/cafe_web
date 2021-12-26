from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('login_check/', views.login_check),
    path('register/', views.register),
    path('register_check/', views.register_check),
    path('findID/', views.findID),
    path('findID_check/', views.findID_check),
    path('findPW/', views.findPW),
    path('findPW_check/', views.findPW_check),
    path('id_overlap_check/', views.id_overlap_check),
]