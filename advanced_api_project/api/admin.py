from django.contrib import admin

# Register your models here.

#from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']  # Display the name field in the admin

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'publication_year', 'author']  # Display relevant fields
