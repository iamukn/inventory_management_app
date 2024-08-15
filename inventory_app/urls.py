#!/usr/bin/python3

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# swagger schema setup

schema_view = get_schema_view(
    openapi.Info(
        title="Inventory Management API",
        default_version='v1',
        description="API documentation for the Inventory Management System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="n.u.kingsley@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("api/v1/products/", include('product.routes')),
    path("api/v1/", include('authentication.routes')),
    path("api/v1/orders/", include('order.routes'))
]


urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

