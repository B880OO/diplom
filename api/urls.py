from django.urls import path

from api.views import *

urlpatterns = [
    path("books/", BookList.as_view()), # Book list
    path("books/<int:pk>/", BookList.as_view()), # Book sorche?
    path("edit/books/<int:pk>/", EditBook.as_view()), # Edit book
    path('ctg/', CategoryList.as_view()), # Category list
    path('ctg/<int:pk>/', CategoryList.as_view()), # Category sorche and delete?
    path('edit/ctg/<int:pk>/', EditCategory.as_view()), # Edit category
    path('pag/ctg/', PagCategory.as_view()), # Pag category
]
