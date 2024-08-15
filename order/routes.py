from django.urls import path
from order.views.order_view import OrderView 
from order.views.order_detail_view import OrderDetailView
from order.views.order_reports import SalesReportView

urlpatterns = [
    path('', OrderView.as_view(), name="orders"),
    path('salesreports', SalesReportView.as_view(), name="salesreport"),
    path('<int:id>/status', OrderDetailView.as_view(), name="order-detail"),
        ]
