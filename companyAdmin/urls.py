from django.urls import path
from . import views

app_name = 'companyAdmin'
urlpatterns = [
    path('', views.new, name='new'),
    path('logout/', views.logout, name='logout'),
    path('visual/', views.visual, name='visual'),
    path('maps/', views.maps, name='maps'),
    path('append/', views.append, name='append'),
    path('delete/', views.delete, name='delete'),
    path('sales_data/', views.sales_data, name='sales_data'),
    path('month/', views.month, name='month'),
    path('location/', views.location, name='location'),
    path('location/detail/', views.location_detail, name='loc_detail'),
    path('append_complete/', views.append_complete, name='append_complete'),
    path('delete_complete/', views.delete_complete, name='delete_complete'),
    path('plist/', views.plist, name='plist')
]