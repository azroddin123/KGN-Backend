from django.contrib import admin
from .models import Category, SubCategory, Store, StorePincode, Product, Inventory, Review, Contact

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_image', 'category_description')
    search_fields = ('category_name',)
    list_filter = ('category_name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'category_image', 'description')
    search_fields = ('name', 'category__category_name',)
    list_filter = ('category',)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'store_admin', 'store_address')
    search_fields = ('store_name', 'store_admin__username', 'store_address')
    list_filter = ('store_admin',)

@admin.register(StorePincode)
class StorePincodeAdmin(admin.ModelAdmin):
    list_display = ('store', 'pincode')
    search_fields = ('store__store_name', 'pincode')
    list_filter = ('store',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'sub_category', 'price', 'description')
    search_fields = ('product_name', 'sub_category__name', 'description')
    list_filter = ('sub_category',)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('store', 'product', 'stock', 'last_updated')
    search_fields = ('store__store_name', 'product__product_name')
    list_filter = ('store', 'product')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'rating', 'description')
    search_fields = ('name', 'email', 'description')
    list_filter = ('rating',)


admin.site.register(Contact)