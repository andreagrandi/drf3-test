from django.conf.urls import url, include
from shop.api import views

urlpatterns = (
    url(r'^orders/$', views.OrdersView.as_view(), name='shop_orders'),
    )
