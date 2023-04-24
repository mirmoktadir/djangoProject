from django.contrib import admin
from django.db.models import Count, QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse

from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')

        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title']
    }
    autocomplete_fields = ["collection"]
    actions = ['clear_inventory']
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    ordering = ["title"]
    list_per_page = 10
    list_select_related = ["collection"]
    list_filter = ['collection', "last_update", InventoryFilter]
    search_fields = ["title"]

    @staticmethod
    def collection_title(product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "Ok"

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products has successfully updated')


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "orders_count"]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_per_page = 10

    @admin.display(ordering="orders_count")
    def orders_count(self, customer):
        url = (
                reverse('admin:store_order_changelist')
                + '?'
                + urlencode(
            {'customer_id': str(customer.id)})

        )
        return format_html('<a href="{}">{}</a>', url,
                           customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ["product"]
    max_num = 10
    min_num = 1
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]
    search_fields = ["title"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
                reverse('admin:store_product_changelist')
                + '?'
                + urlencode(
            {'collection_id': str(collection.id)})

        )
        return format_html('<a href="{}">{}</a>', url,
                           collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )
