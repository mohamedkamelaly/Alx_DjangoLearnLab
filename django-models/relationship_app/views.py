from django.shortcuts import render
from django.views.generic import ListView
from .models import Book
# Create your views here.
def book_list(request):
    """Retrieves all books and renders a template displaying the list."""
    books = Book.objects.all()  # Fetch all book instances from the database
    context = {'book_list': books}
    return render(request, 'books/book_list.html', context)

class library_list(ListView):
    model = Book
    template_name = 'books/library_list.html'


    
