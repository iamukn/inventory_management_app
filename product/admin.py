from django.contrib import admin
from product.models import Products

# register the model to admin
#admin.site.register(Products)

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


admin.site.site_header = "Inventory Management"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome! 😎"
