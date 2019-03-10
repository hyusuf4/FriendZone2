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

def public_posts(request):
    pass

def author_post(request):
    pass

def post_details(request):
    pass
def post_comments(request):
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
