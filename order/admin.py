from django.contrib import admin
from order.models import Orders

@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','total', 'date_of_purchase')  # Columns to display in the list view
    search_fields = ('id',)  # Fields to include in the search box
    list_filter = ('date_of_purchase',)  # Filters on the right sidebar
