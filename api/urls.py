from django.urls import path

from api.views import *

urlpatterns = [
    path("books/", BookList.as_view()),
    path("books/<int:pk>/", BookList.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='login'),
    path('reg/', UserCreateView.as_view(), name='login'),
]
