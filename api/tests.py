from django.test import TestCase
from django.utils import timezone
from .models import Author, FriendRequest, Friends,Post,Comment, Following
from django.test import Client
from django.urls import reverse
from django.db.models import Q

""""""
from api.models import Author, FriendRequest, Friends,Post,Comment
from api.serializers import AuthorSerializer, FriendRequestSerializer, FriendsSerializer,PostSerializer,CommentSerializer, FollowingSerializer
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.utils.timezone import get_current_timezone, make_aware
from django.core import serializers
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import IsAuthenticated
import sys
import unittest
from django.utils import timezone
import pytz
""""""

from .views import enroll_following, make_them_friends, unfollow

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

# reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}), {'renewal_date':valid_date_in_future})
class LoginViewTest(TestCase):
    def test_login(self):
        # response = self.client.login(username="admin", password="admin")
        data = {'username': 'u1','password': 'u1', 'email':'a@b.ca'}
        response = self.client.post(reverse('api:signup'), data=data, format='json')
        print(response)
        self.assertEqual(response.status_code, 200)

class FriendRequestViewTests(TestCase):
    def test_create_first_frequest(self):
        pass
    def test_create_duplicate_frequest(self):
        pass
    def test_make_friends(self):
        pass

def CheckFriendshipViewTests(TestCase):
    def test_existing_friendship(self):
        response = self.client.get(reverse('api:author/<authorid>/friends/<authorid2>/', kwargs={}))

class FriendResultViewTests(TestCase):
    pass

class UnfriendViewTests(TestCase):
    pass

class UtilityTests(TestCase):
    def test_getAuthor(self):
        # Asserts Author is being created
        try:
            a1 = Author.objects.create(firstName='test_user', lastName='test_user_lastname', userName='test_userName', password='test')

            self.assertTrue(Author.objects.get(firstName='test_user'))
            self.assertTrue(Author.objects.get(userName='test_userName'))


        except Exception as e:
            print("Error!!!")

    def test_createPost(self):
        try:
            a1 = Author.objects.create(firstName='test_user', lastName='test_user_lastname', userName='test_userName', password='test')
            self.assertTrue(Author.objects.get(firstName='test_user'))
            self.assertTrue(Author.objects.get(userName='test_userName'))

        except Exception as e:
            print("Error!!!")

        p1 = Post.objects.create(publicationDate= timezone.now() ,content='this is a test', title='test', permission = "P", author = a1)

        self.assertTrue(Post.objects.get(title='test'))





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
            #print("Saved")
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
            result = Friends.objects.filter( Q(author1=a1, author2=a2) | Q(author2=a1, author1=a2)).exists()

            self.assertTrue(result)
            # print(111,Friends.objects.filter( Q(author1=a1), Q(author2=a2) | Q(author2=a1), Q(author1=a2)),222)
        except Friends.DoesNotExist:
            result = False
        self.assertTrue(result)


    def test_enroll_following(self):
        a1 = create_author(f_name="a1", l_name="a1", u_name="101", pwd=101)
        a1.save()
        a2 = create_author(f_name="a2", l_name="a2", u_name="102", pwd=101)
        a2.save()
        temp_dict = {"requester_id" :a1 , "requestee_id":a2}
        enroll_following(temp_dict)
        try:
            result = Following.objects.filter(follower=a1, following=a2)
        except Friends.DoesNotExist:
            result = False
        self.assertTrue(result)

    def test_unfollow(self):
        a1 = create_author(f_name="a1", l_name="a1", u_name="101", pwd=101)
        a1.save()
        a2 = create_author(f_name="a2", l_name="a2", u_name="102", pwd=101)
        a2.save()
        temp_dict = {"requester_id" :a1 , "requestee_id":a2}
        enroll_following(temp_dict)
        temp_dict = {"follower" :a1 , "following":a2}
        unfollow(temp_dict)
        try:
            result = Following.objects.filter(follower=a1, following=a2).exists()
            #print(result)
        except Friends.DoesNotExist:
            result = True
        self.assertFalse(result)
