from django.shortcuts import render
from rest_framework import generics
from .serializers import BookSerializer
from .models import Book
# Create your views here.

#A ListView for retrieving all books.
class ListView(generics.ListApiView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

#A DetailView for retrieving a single book by ID.
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
#A CreateView for adding a new book.
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
#An UpdateView for modifying an existing book.
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

#A DeleteView for removing a book.
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer