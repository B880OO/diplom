from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
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
