from django.contrib import admin
from .models import Order, Product, User
from import_export.admin import ImportExportMixin
from import_export import resources

# admin.site.register(Order)
admin.site.register(Product)
admin.site.register(User)


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('id', 'user__email', 'user__first_name', 'user__last_name', 'fixed_amount')


class OrderAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = OrderResource

admin.site.register(Order, OrderAdmin)
