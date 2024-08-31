from django.urls import path
from .views import BookList

urlpatterns = [
    path("api/books", BookList.as_view(), name = "Book_create_List")

]