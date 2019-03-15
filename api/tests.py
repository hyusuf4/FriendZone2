from django.test import TestCase
from django.utils import timezone
from .models import Author, FriendRequest, Friends,Post,Comment, Following
from django.test import Client
from django.urls import reverse
from django.db.models import Q

""""""
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
""""""

# Create your tests here.
def create_author(f_name="A", l_name="B", u_name="101", pwd=101):
    return Author.objects.create(\
        firstName=f_name,\
        lastName=l_name,\
        userName=u_name,\
        password=pwd
    )

def create_friend_request(author_one, author_two):
    return FriendRequest.objects.create(\
        from_author=author_one,\
        to_author=author_two,\
        created=timezone.now()
    )

class FriendRequestViewTests(TestCase):
    def test_create_first_frequest(self):
        pass
    def test_create_duplicate_frequest(self):
        pass
    def test_make_friends(self):
        pass

class FriendResultViewTests(TestCase):
    pass

class UnfriendViewTests(TestCase):
    pass

class UtilityTests(TestCase):
    def test_make_them_friends(self):
        a1 = create_author(f_name="a1", l_name="a1", u_name="101", pwd=101)
        a1.save()
        a2 = create_author(f_name="a2", l_name="a2", u_name="102", pwd=101)
        a2.save()
        fr = create_friend_request(a1, a2)
        fr.save()
        make_them_friends(a1, a2, fr)

        try:
            check_user = Author.objects.get(pk=a2.pk)
            print("Saved")
        except Exception as e:
            print("Error!!")

        # no friend request
        result0 = False
        try:
            result0 = FriendRequest.objects.get(pk=fr.pk).exists()
        except FriendRequest.DoesNotExist:
            result0 = False
        self.assertFalse(result0)
        # have entry in friends
        result = False
        try:
            result = Friends.objects.filter( Q(author1=a1, author2=a2) | Q(author2=a1, author1=a2))
            # result = Friends.objects.filter(author1=a1)
            # r = Friends.objects.get(author1=a1.pk)
            # r = Friends.objects.all()

            print(111, result.values())
            # print(111,Friends.objects.filter( Q(author1=a1), Q(author2=a2) | Q(author2=a1), Q(author1=a2)),222)
        except Friends.DoesNotExist:
            result = False
        self.assertTrue(result)


    def test_enroll_following(self):
        pass
    def test_unfollow(self):
        pass

def make_them_friends(author_one, author_two, existing_request):
    # change status of a friend request
    existing_request.accepted = True
    existing_request.regected = False
    # create instance of Friends
    temp_dict = {"from_author" :existing_request.from_author , "to_author":existing_request.to_author}
    # print(existing_request.from_author.pk)
    serializer = FriendsSerializer(data=temp_dict)
    serializer.create(temp_dict)
    existing_request.delete()

    if serializer.is_valid():
        return Response(serializer.data)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
