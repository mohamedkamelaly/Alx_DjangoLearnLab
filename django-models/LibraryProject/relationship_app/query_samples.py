from .models import Author, Book, Library, Librarian
author = Author.objects.get(name=author_name)
books = Book.objects.filter(author=author)
library = Library.objects.get(name=library_name)
books = Book.objects.filter(library=library)

