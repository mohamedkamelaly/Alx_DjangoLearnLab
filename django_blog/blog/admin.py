from django.contrib import admin
from .models import Post , MyUser
# Register your models here.
class AdminPost(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'author')   #admin.site.register(Post, AdminPost)

class AdminUser(admin.ModelAdmin):
    list_display = ('username', 'email')


admin.site.register(Post, AdminPost)
admin.site.register(MyUser, AdminUser)

