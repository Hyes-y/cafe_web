from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('', views.index, name='index'),
    path('shopsel/<str:c_code>', views.shopsel, name='shopsel'),
    path('product/', views.product, name='product'),
    path('<str:p_code>/option/', views.option, name='option'),
    path('<str:p_code>/cart_save/', views.cart_save, name='cart_save'),
    path('<str:product_id>/cart_remove/', views.cart_remove, name='cart_remove'),
    path('remove/', views.remove, name='remove'),
    path('cart/', views.cart, name='cart'),
]
