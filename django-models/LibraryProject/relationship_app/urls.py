from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_list, name='book'),
    path('library/', views.library_list.as_view(), name='library'),
]