from django.contrib import admin
from .models import Order, Product, User
from import_export.admin import ImportExportModelAdmin

# admin.site.register(Order)
admin.site.register(Product)
admin.site.register(User)


class OrderAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Order, OrderAdmin)
