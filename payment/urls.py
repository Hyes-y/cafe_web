from django.urls import path
from payment import views

app_name = 'payment'
urlpatterns = [
    path('', views.index, name='index'),
    path('pay/', views.pay),
    path('<int:cart_id>/approval/', views.approval, name='approval'),
    path('fail/', views.fail),
    path('cancel/', views.cancel),
    path('complete/', views.complete, name='complete'),
    path('pay_history/', views.pay_history, name='history'),
]