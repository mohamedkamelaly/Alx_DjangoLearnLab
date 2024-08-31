from django.urls import path
from .views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'my-models', BookViewSet)


urlpatterns = [
    path("books/", BookList.as_view(), name = "Book_create_List"),
    path('api/', include(router.urls)),

]