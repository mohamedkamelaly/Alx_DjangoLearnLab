from django.shortcuts import render
from .models import Book
from django.utils import timezone
# Create your views here.
def create_Book(request):
    Book.objects.create(title= "1984", author= "George Orwell",publication_year= 1949)
    #SELECT * from Book
    Book.objects.all()
