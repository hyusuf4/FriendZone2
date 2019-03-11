from api.models import Author, FriendRequest, Friends,Post,Comment
from api.serializers import AuthorSerializer, FriendRequestSerializer, FriendsSerializer,PostSerializer,CommentSerializer
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.utils.timezone import get_current_timezone, make_aware
from django.core import serializers
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
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
@permission_classes((IsAuthenticated,))
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

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def public_posts(request):
    if request.method == 'GET':
        post = Post.objects.all()
        serializer = PostSerializer(post,many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT','POST'])
@permission_classes((IsAuthenticated,))
def author_post(request,pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        post= Post.objects.filter(author=pk)
        serializer = PostSerializer(post,many=True)
        return Response(serializer.data)

    
@api_view(['GET', 'PUT','DELETE'])
@permission_classes((IsAuthenticated,))
def post_details(request,pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        post= Post.objects.filter(postid=pk)
        serializer = PostSerializer(post,many=True)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data=JSONParser().parse(request)
        data['publicationDate']=parse_datetime(data['publicationDate'])
        serializer = PostSerializer(Post,data=data)
        if serializer.is_valid():
            serializer.update(post,data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif  request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def post_comments(request,pk):
    pass

"""from_pk is friend reuquest creater's pk, to_pk is friend reuquest receiver's pk  """
""" request is JSON: from_pk:***, to_pk:***"""
@api_view(['POST'])
def friend_request(request):
    # model: FriendRequest

    if request.method != 'POST':
        # invalid method
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    """ TODO: check whether there is already an friend request"""
    """ if yes then make friends, else execute this method"""

    # insert new entry in database
    data= JSONParser().parse(request)
    # print("1111111", data.get('from_pk'))
    # print("2222222", data.get('to_pk'))
    serializer = FriendRequestSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # friend_request_instance = FriendRequest.objects.create(from_author = 'from_pk', to_author = 'to_pk')

    """ TODO: update the following table in DB"""

    """ TODO: user story => As an author, I want to know if I have friend requests."""

    return Response(status=status.HTTP_201_CREATED)

def friend_result():
    """ modify friend request entry values (accept and reject)"""
    """ user would get notification about requests are not rejected"""
    pass

def unfriend():
    """ TODO: 1, remove from friend list | 2, remove from following list"""
    pass

"""some ideas about friends of friends: """
""" create friend list for each author, make them set, and then count intersection of them"""
