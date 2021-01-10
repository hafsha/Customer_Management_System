from django.urls import path
from .import views

urlpatterns = [
    path('',views.home, name='home'),
    path('products/',views.products, name='products'),
    path('customers/<int:pk>/',views.customers, name='customers'),
    
    path('create_order/<int:pk>/', views.createOrder, name='create_order'),
    path('update_order/<int:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<int:pk>/', views.deleteOrder, name='delete_order'),
]