from api.models import Author, FriendRequest, Friends,Post,Comment
from api.serializers import AuthorSerializer, FriendRequestSerializer, FriendsSerializer,PostSerializer,CommentSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.core import serializers


@api_view(['GET', 'POST'])
def authors_list(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def author_details(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data= JSONParser().parse(request)
        serializer = AuthorSerializer(Author, data=data)
        if serializer.is_valid():
            serializer.update(author,data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def public_posts(request):
    try:
        posts = Post.objects.all()
        print(posts)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # elif request.method == 'POST':
    #     data= JSONParser().parse(request)
    #     serializer = PostSerializer(Post, data=data)
    #     if serializer.is_valid():
    #         serializer.update(posts,data)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def author_post(request):
    pass

def post_details(request):
    pass
def post_comments(request,pk):
    try:
         #= Question.objects.filter(user=request.user).values()
        posts = Post.objects.get(pk=pk)
        print(posts)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # elif request.method == 'POST':
    #     data= JSONParser().parse(request)
    #     serializer = PostSerializer(Post, data=data)
    #     if serializer.is_valid():
    #         serializer.update(posts,data)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def friend_request(request):
    pass