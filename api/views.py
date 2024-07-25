from .serializers import UserSerializer
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from api.models import Book

# Create your views here.
class BookList(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            try:
                book = get_object_or_404(Book, pk=pk)
                return Response({"book":model_to_dict(book)})
            except Exception as e:
                return Response(
                    {"error":{"message":"Bad Request","status":"INVALID_ARGUMENT","details":str(e)}}
                )
        else:
            books = Book.objects.all().values()
            return Response({"books": list(books)})

    def post(self,request, *args, **kwargs):
        try:
            new_book = Book.objects.create(
                title=request.data['title'],
                author=request.data['author'],
                category_id=request.data['category_id']
            )
            return Response({"book": model_to_dict(new_book)})
        except Exception as e:
            return Response(
                {"error": {"message": "Bad Request", "status": "INVALID_ARGUMENT", "details": str(e)}}
            )
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
    
class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
