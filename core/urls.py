from django.urls import path
from .views import HomeView, ItemDetailView, add_to_cart, remove_from_cart, remove_single_item_from_cart, OrderSummaryView, CheckoutView, OrderComplete



urlpatterns = [
    
    path('', HomeView.as_view(), name = 'home'),
    path('product/<slug>', ItemDetailView.as_view(), name = 'product'),
    path('add-to-cart/<slug>', add_to_cart, name = 'add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name = 'remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name = 'order-summary'),
    path('remove_single_item_from_cart/<slug>', remove_single_item_from_cart, name = 'remove_single_item_from_cart'),
    path('checkout/', CheckoutView.as_view(), name = 'checkout'),
    path('order-complete', OrderComplete, name  ='order-complete')
]
