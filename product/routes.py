#!/usr/bin/python3
from django.urls import path
from product.views.products_view import Products_view as Products
from product.views.product_detail_view import ProductDetailView
from product.views.product_report_view import ProductsReportView

# routers for the product app

urlpatterns = [
    path('', Products.as_view(), name='products'),
    path('<int:id>', ProductDetailView.as_view(), name='product'),
    path('stockreports', ProductsReportView.as_view(), name='stockreports')
        ]
