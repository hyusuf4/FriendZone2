from api.models import Author, FriendRequest, Friends,Post,Comment,VisibleToPost
from api.serializers import AuthorSerializer, FriendRequestSerializer, FriendsSerializer,PostSerializer,CommentSerializer,VisibleToPostSerializer
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.utils.timezone import get_current_timezone, make_aware
from django.core import serializers
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.db.models import Q


@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticated,))
def authors_list(request):
    authors_to_pass=[]
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        #queryset = Author.objects.all().values_list('userName',flat=True)
        
        
        #print(queryset[0])
        users_search = JSONParser().parse(request)
        print("**********************************************************************")
        print(users_search['users_search'])
        users_search=users_search['users_search']
        if users_search is not "":
            #print(queryset)
            queryset=Author.objects.filter(Q(userName__startswith=users_search))
            #queryset = queryset.filter(userName=users_search['users_search']).values_list('userName',flat=True)
            print("**********************************************************************")
            print("**********************************************************************")
            print("**********************************************************************")
            print("**********************************************************************")
            """ for q in queryset:
                author = Author.objects.get(userName=q)
                print("here is the serializer")
                serializer = AuthorSerializer(author)
                print(serializer.data) """
            print(queryset)
        
            for q in queryset:
                print(type(q))
                #author = Author.objects.get(userName=q)
                #print(type(author))
                serializer = AuthorSerializer(q)
                print(serializer.data)
                authors_to_pass.append(serializer.data)


            
            return Response(authors_to_pass)
        else:
            serializer = AuthorSerializer(authors,many=True)
            return Response(serializer.data)
       

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
            return Response({"query":"update Post","success":True},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','POST'])
def post_visibleToAuth(request):
    try:
        author=Author.objects.get(owner=request.user)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    if request.method == "GET":
        posts=[]
        visiblePosts=VisibleToPost.objects.filter(author=author)
        for post in visiblePosts:
            v_posts=Post.objects.filter(postid=post)
            posts.append(posts)
        return Response({"query":"authorized posts","posts":posts},status=status.HTTP_200_OK)
    
    if request.method == "POST":
        data=JSONParser().parse(request)
        serializer=PostSerializer(Post,data=data)
        if serializer.is_valid():
            serializer.create(data,author)
            return Response({"query":"Add Post", "success":True}, status=status.HTTP_200_OK)
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
    return JsonResponse(request.user, safe=False)
    if request.user == author.owner:
        if request.method == 'GET':
            post= Post.objects.filter(author=pk)
            serializer = PostSerializer(post,many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            serializer=PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        if request.method == 'GET':
            post= Post.objects.filter(Q(author))



    
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
