from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/<int:property_id>/', views.property_detail, name='property_detail'),
    path('properties/type/<int:property_type_id>/', views.property_list_by_type, name='property_list_by_type'),
    path('about', views.about, name='about'),
    path('search/', views.search_results, name='search_results'),
    path('contact/', views.contact, name='contact'),
    path('contact_success/', views.contact_success, name='contact_success'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:property_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('payments/create-order/<int:property_id>/', views.create_order, name='create_order'),
    path('payments/payment-success/', views.payment_success, name='payment_success'),
    path('payments/success/', views.payment_success_page, name='payment_success_page'),
]

