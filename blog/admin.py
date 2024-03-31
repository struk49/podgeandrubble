from django.contrib import admin
from .models import Blog_post, Category

# Register your models here.

class Blog_postAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'image',
    )

    ordering = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

admin.site.register(Blog_post, Blog_postAdmin)
admin.site.register(Category, CategoryAdmin)