from django.shortcuts import render
from .serializers import BookSerializers
from rest_framework import generics
from .models import Book
# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers