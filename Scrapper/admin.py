from django.contrib import admin
from .models import Brand, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ProductInline]
