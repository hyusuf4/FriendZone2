from api.models import Author, FriendRequest, Friends,Post,Comment,VisibleToPost
from api.serializers import AuthorSerializer, FriendRequestSerializer, FriendsSerializer,PostSerializer,CommentSerializer,VisibleToPostSerializer,CategoriesSerializer
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.utils.timezone import get_current_timezone, make_aware
from django.core import serializers
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
from .pagination import DefaultPageNumberPagination
from rest_framework.settings import api_settings
import json

class ListAuthors(APIView):
    """
    API View to list all authors in the system
    Requires token authentication.
    """

    #permission_classes = (IsAuthenticated,)
    serializer_class=AuthorSerializer
    pagination_class= DefaultPageNumberPagination

    def post(self,request,format=None):
        authors_to_pass=[]
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
                print(q)
                author = Author.objects.get(userName=q)
                serializer = AuthorSerializer(author)
                print(serializer.data)
                authors_to_pass.append(serializer.data)
            return Response(authors_to_pass)
        else:
            serializer = AuthorSerializer(authors,many=True)
            return Response(serializer.data)

    def get(self,request):
        authors=Author.objects.all().order_by('-pk')
        serializer = AuthorSerializer(authors,many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        return {"request": self.request}

class AuthorDetails(APIView):
    """
    API view to show details of specified author
    Requires token authentication.
    """
    #permission_classes = (IsAuthenticated,)
    def get_author(self,request,pk):
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return "error"
        return author

    def get(self, request, pk, format=None):
        """Returns author <id=pk> details.
        """
        author=self.get_author(request,pk)
        if author=="error":
            return Response({"query":"posts","success":False,"message":"Cannot find author"},status=status.HTTP_200_OK)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    def put(self, request,pk, format=None):
        """Updates author details if he/she is an authenticated user.
        """
        author=self.get_author(request,pk)
        if author=="error":
            return Response({"query":"posts","success":False,"message":"Cannot find author"},status=status.HTTP_200_OK)
        if pk == str(author.pk):
            data= JSONParser().parse(request)
            serializer = AuthorSerializer(Author, data=data)
            if serializer.is_valid():
                serializer.update(author,data)
                return Response({"query":"Update Author Details","success":True,"message":"Updated Information"},status=status.HTTP_200_OK)
            return Response({"query":"Update Author Details","success":False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"query":"Update Author Details","success":False, "message":"this is not your profile"}, status=status.HTTP_400_BAD_REQUEST)


class PostOfAuth(APIView):
    """
    API view to list all posts visible to authenticated user
    Requires token authentication.
    """
    pagination_class= DefaultPageNumberPagination
    #permission_classes = (IsAuthenticated,)
    def get_author(self,request):
        try:
            author=Author.objects.get(owner=request.user)
        except Author.DoesNotExist:
            return "error"
        return author


    def get(self,request,format=None):
        posts=[]
        author=self.get_author(request)
        if author=="error":
            return Response({"query":"posts","success":False,"message":"Cannot find author"},status=status.HTTP_200_OK)
        visiblePosts=VisibleToPost.objects.filter(author=author).values('post_id')
        print(visiblePosts)
        for post in visiblePosts:
            v_posts=Post.objects.filter(Q(postid=post['post_id'])| Q(author=author))
            serializer=PostSerializer(v_posts,many=True)
            posts.append(serializer.data)
        return JsonResponse({"query":"posts","posts":posts})


    def get_serializer_context(self):
        return {"request": self.request}


    def post(self,request,format=None):
        author=self.get_author(request)
        if author=="error":
            return Response({"query":"posts","success":False,"message":"Cannot find author"},status=status.HTTP_200_OK)
        data=JSONParser().parse(request)
        serializer=PostSerializer(Post,data=data)
        if serializer.is_valid():
            serializer.create(data,author)
            return Response({"query":"Add Post", "success":True ,"message":"Added a New Post"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicPosts(APIView):
    """
    API view to list all public posts
    Requires token authentication.
    """

    #permission_classes = (IsAuthenticated,)
    pagination_class= DefaultPageNumberPagination
    def get(self, request,format=None):
        post = Post.objects.all().filter(permission="P")
        serializer = PostSerializer(post,many=True)
        return Response(serializer.data)



class PostOfAuthors(APIView):
    """
    API view to list post of a certain author visble to authenticated user
    Requires token authentication.
    Only GET IS ALLOWED HERE
    """
    def get_author(self,request):
        try:
            author=Author.objects.get(owner=request.user)
        except Author.DoesNotExist:
            return "error"
        return author

    #permission_classes = (IsAuthenticated,)
    pagination_class= DefaultPageNumberPagination
    def get(self, request,pk,format=None):
        author=self.get_author(request)
        if author=="error":
            return Response({"query":"posts","success":False,"message":"Cannot find author"},status=status.HTTP_200_OK)
        posts=[]
        postids = VisibleToPost.objects.filter(author=author).values('post_id')
        for id in postids:
            post=Post.objects.filter(Q(postid=id['post_id']) & Q(author_id=pk))
            posts.append(serializer.data)
        serializer = PostSerializer(posts,many=True)
        return Response({"query":"posts","posts":posts},status=status.HTTP_200_OK)



class PostDetails(APIView):
    """
    API view give you details of a specific post given by id
    Requires token authentication.

    GET PUT DELETE OPERATIONS ALLOWED HERE
    """

    def get_author(self,request):
        try:
            author=Author.objects.get(owner=request.user)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return author

    def get_post(self,pk):
        try:
            post=Post.objects.get(postid=pk)
        except Post.DoesNotExist:
            return "error"
        return post

    def get(self, request,pk,format=None):
        post=self.get_post(pk)
        if post=="error":
            return Response({"query":"posts","success":False,"message":"Cannot find post"},status=status.HTTP_200_OK)
        else:
            serializer=PostSerializer(post)
            return Response({"query":"posts","success":True,"posts":serializer.data},status=status.HTTP_200_OK)

    def put(self,request,pk,format=None):
        author= self.get_author(request)
        post=self.get_post(pk)
        if post=="error":
            return Response({"query":"posts","success":False,"message":"Cannot find post"},status=status.HTTP_200_OK)
        if author == post.author:
            data=JSONParser().parse(request)
            serializer = PostSerializer(post,data=data)
            if serializer.is_valid():
                serializer.update(post,data)
                return Response({"query":"Update Users Post","success":True, "message":"Updated your post"},status=status.HTTP_200_OK)
            return Response({"query":"Update Users Post","success":True, "message":serializer.errors},status=status.HTTP_200_OK)
        else:
            return Response({"query":"Update Users Post","success":False, "message":"Sorry this is not your post to update"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        author=self.get_author(request)
        post=self.get_post(pk)
        if author==post.author:
            post.delete()
            return Response({"query":"Delete Users Post","success":True, "message":"Deleted your post"},status=status.HTTP_200_OK)
        else:
            return Response({"query":"Delete Users Post","success":False, "message":"Sorry this is not your post to delete"}, status=status.HTTP_400_BAD_REQUEST)


class PostComments(APIView):
    """
    API view give you details of a specific post given by id
    Requires token authentication.

    GET PUT DELETE OPERATIONS ALLOWED HERE
    """
    def get_author(self,request):
        try:
            author=Author.objects.get(owner=request.user)
        except Author.DoesNotExist:
            return "error"
        return author

    def get_comment(self,post):
        return Comment.objects.filter(postid=post)

    def get_post(self,pk):
        try:
            post=Post.objects.get(postid=pk)
        except Post.DoesNotExist:
            return "error"
        return post

    def get(self, request,pk,format=None):
        post=self.get_post(pk)
        if post=="error":
            return Response({"query":"posts","success":False,"message":"Cannot find post"},status=status.HTTP_200_OK)
        else:
            comments=self.get_comment(post)
            serializer=CommentSerializer(comments,many=True)
            return Response({"query":"Get Post Comments","success":True,"comments":serializer.data},status=status.HTTP_200_OK)

    def post(self,request,pk,format=None):
        author=self.get_author(request)
        post=self.get_post(pk)
        if post=="error":
            return Response({"query":"posts","success":False,"message":"Cannot find post"},status=status.HTTP_200_OK)
        data=JSONParser().parse(request)
        serializer=CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.create(data,author,post)
            return Response({"query":"Create Comment", "success":True ,"message":"Comment Created"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FriendRequest(APIView):
    def post(self,request):
        data= JSONParser().parse(request)
        serializer = FriendRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'query':"Send friendRequest",'success':True,'message':"Friend Request sent"},status=status.HTTP_200_OK)
        else:
            return Response({'query':"Send friendRequest",'success':True,'message':serializers.errors}, status=status.HTTP_400_BAD_REQUEST)




def friend_result():
    """ modify friend request entry values (accept and reject)"""
    """ user would get notification about requests are not rejected"""
    pass

def unfriend():
    """ TODO: 1, remove from friend list | 2, remove from following list"""
    pass

"""some ideas about friends of friends: """
""" create friend list for each author, make them set, and then count intersection of them"""
