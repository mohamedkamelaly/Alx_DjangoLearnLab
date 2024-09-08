from django.test import TestCase
from .models import Book
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from .views import ListView, BookDetailView
from django.urls import reverse
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.url = reverse('book-list')
        self.book = Book.objects.create(title = 'GOT', publication_year = 2024)
    # Create initial book data
    def test_book_list(self):
        response = self.client.get (self.url)
        self.assertEqual(response.status_code, 200)   
        titles = [title ['title'] for title in response.data]
        self.assertIn('GOT', titles)