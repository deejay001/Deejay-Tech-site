from django.contrib import admin
from .models import Category, Post, Comment


# Register your models here.


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('title', 'created_on')


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ('title', 'image', 'author', 'created_on', 'updated_on', 'status')
    list_filter = ('status',)
    search_fields = ['title', 'author', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_on', 'active')
    list_filter = ('active',)
    search_fields = ['name', 'body']
    actions = ['approve_comment']

    @staticmethod
    def approve_comment(self, request, queryset):
        queryset.update(active=True)
