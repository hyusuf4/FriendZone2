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
import sys


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

    if request.method != 'POST':
        # invalid method
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    # insert new entry in database
    data = JSONParser().parse(request)
    requester_id = data.get('from_author')
    requestee_id = data.get('to_author')

    """ TODO: check whether there is already an friend request"""
    """ if yes make friends"""
    try:
        existing_request = FriendRequest.objects.get(to_author=requester_id, from_author=requestee_id)
        """make them friends"""
        enroll_following(requester_id, requestee_id)
        return make_them_friends(requester_id, requestee_id, existing_request)
    except FriendRequest.DoesNotExist:
        pass
    except FriendRequest.MultipleObjectsReturned:
        print("Error: duplicate instances in DB", file=sys.stderr)

    """ check duplicate requests"""
    try:
        existing_request = FriendRequest.objects.get(from_author=requester_id, to_author=requestee_id)
        return Response(serializer.data)
    except FriendRequest.DoesNotExist:
        pass
    except FriendRequest.MultipleObjectsReturned:
        print("Error: duplicate instances in DB", file=sys.stderr)

    """fresh request, implement it"""
    serializer = FriendRequestSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    temp_dict = {"requester_id" :requester_id , "requestee_id":requestee_id}
    enroll_following(temp_dict)

    """ TODO: user story => As an author, I want to know if I have friend requests."""

    return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
def friend_result(request):
    """ modify friend request entry values (accept and reject)"""
    if request.method != 'POST':
        # invalid method
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    data = JSONParser().parse(request)
    try:
        req = FriendRequest.objects.get(from_author=data.from_author, to_author=data.to_author)
    except FriendRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = FriendRequestSerializer(FriendRequest,data=data)
    if serializer.is_valid():
        serializer.update(req,data)
    """ TODO user would get notification about requests are not rejected"""

@api_view(['POST'])
def unfriend(request, pk):
    if request.method != 'POST':
        # invalid method
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    """ TODO: 1, remove from friend list | 2, remove from following list"""
    # delete from friend list
    data = JSONParser().parse(request)
    try:
        req = Friends.objects.get(author1=data.author1, author2=data.author2)
    except FriendRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    req.delete()

    if data.author1 == pk:
        following = author2
    else:
        following = data.author1

    if not unfollow(pk, following):
        print("Error: following instance is not found", file=sys.stderr)
    return Response(status=status.HTTP_200_OK)


"""some ideas about friends of friends: """
""" create friend list for each author, make them set, and then count intersection of them"""

"""***************************Utility*************************"""
def make_them_friends(author_one, author_two, existing_request):
    # change status of a friend request
    existing_request.accepted = True
    existing_request.regected = False
    temp_dict = {"from_author" :existing_request.from_author , "to_author":existing_request.to_author}
    # create instance of Friends
    serializer = FriendsSerializer(data=temp_dict)
    serializer.create(temp_dict)
    existing_request.delete()

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def enroll_following(validated_data):
    """TODO check duplicate here"""
    serializer = FollowingSerializer(data=validated_data)
    serializer.create(validated_data)
    if serializer.is_valid():
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def unfollow(validated_data):
    try:
        req = Following.objects.get(follower=validated_data.get("follower"), following=validated_data.get("following"))
    except Following.DoesNotExist:
        return False
    req.delete()
    return True







#
