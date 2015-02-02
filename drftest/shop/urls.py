from django.conf.urls import url
from shop.api import views

urlpatterns = (
    url(r'^orders/$', views.OrdersView.as_view(), name='shop_orders'),
    url(r'^stamps/$', views.StampsView.as_view(), name='shop_stamps'),
    url(r'^vouchers/$', views.VouchersView.as_view(), name='shop_vouchers'),
    )
