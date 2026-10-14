# File: apps/cart_orders/apps.py
from django.apps import AppConfig


class CartOrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cart_orders'
    label = 'cart_orders'
