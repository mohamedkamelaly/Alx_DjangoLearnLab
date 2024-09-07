from django.shortcuts import render
from rest_framework import generics
from .serializers import BookSerializer
from .models import Book
from django_filters import rest_framework
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated"
from rest_framework.exceptions import ValidationError
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.

#A ListView for retrieving all books.
class ListView(generics.ListApiView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author', 'publication_year']  # Example: Filter by author or publication year
    search_fields = ['title']  # Example: Search by title
    ordering_fields = ['title', 'publication_year']

#A DetailView for retrieving a single book by ID.
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
#A CreateView for adding a new book.
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Custom validation or processing before saving
        title = serializer.validated_data.get('title')
        publication_year = serializer.validated_data.get('publication_year')

        if Book.objects.filter(title=title).exists():
            raise ValidationError("A book with this title already exists.")
        serializer.save()
        
#An UpdateView for modifying an existing book.
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Example: Only authenticated users can update

    def perform_update(self, serializer):
        # Custom validation or processing before updating
        publication_year = serializer.validated_data.get('publication_year')
        
        if publication_year > datetime.now().year:
            raise ValidationError("Publication year cannot be in the future.")
        
        # Save after custom validation or processing
        serializer.save()

#A DeleteView for removing a book.
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer