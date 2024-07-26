from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from api.models import Book, Category
from api.serializers import CategorySerializer

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
        
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
class EditBook(APIView):
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        book = get_object_or_404(Book, pk=pk)
        book.title = request.data.get("title", book.title)
        book.author = request.data.get("auther", book.author)
        book.category_id = request.data.get("category_id", book.category_id)
        book.save()
        return Response({"book": model_to_dict(book)})

class CategoryList(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            try:
                ctg = get_object_or_404(Category, pk=pk)
                return Response({"Category":model_to_dict(ctg)})
            except Exception as e:
                return Response(
                    {"error":{"message":"Bad Request","status":"INVALID_ARGUMENT","details":str(e)}}
                )
        else:
            ctg = Category.objects.all().values()
            return Response({"Category": list(ctg)})
        
    def post(self,request, *args, **kwargs):
        try:
            new_ctg = Category.objects.create(
                title=request.data['title'],
            )
            return Response({"Category": model_to_dict(new_ctg)})
        except Exception as e:
            return Response(
                {"error": {"message": "Bad Request", "status": "INVALID_ARGUMENT", "details": str(e)}}
            )

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        book = get_object_or_404(Category, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
class EditCategory(APIView):
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        ctg = get_object_or_404(Category, pk=pk)
        ctg.title = request.data.get("title", ctg.title)
        ctg.save()
        return Response({"Category": model_to_dict(ctg)})

class PagCategory(APIView):
    def get(self, request):
        categories = Category.objects.all()
        paginator = PageNumberPagination()
        page_categories = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(page_categories, many=True)
        return paginator.get_paginated_response(serializer.data)
