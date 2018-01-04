from django.contrib import admin
from .models import Post
#Register your models here.

class CustomAdminPosts(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'timeStamp', 'update']
    list_display_links = ['title']
    search_fields = ['title','content']
    class Meta:
        model=Post

admin.site.register(Post, CustomAdminPosts)