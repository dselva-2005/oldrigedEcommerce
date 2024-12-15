from django.contrib import admin
from .models import Category, Product, ProductImage, SiteReviewModel, ProductReview
# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty image fields to display by default
    fields = ['image','name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','created','updated','price','available']
    list_filter = ['created','available','updated']
    list_editable = ['price','available']
    prepopulated_fields = {'slug':('name',)}
    inlines = [ProductImageInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product','name','image',]
    list_editable = ['image']
    list_filter = ['product']


@admin.register(SiteReviewModel)
class SiteReviewModelAdmin(admin.ModelAdmin):
    list_display = ['rating','created',]
    list_filter = ['created']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product','rating','created',]
    list_filter = ['product','created']