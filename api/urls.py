from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .api import RegisterAPI,LoginAPI,UserAPI
from knox import views as knox_views
from .views import ListAuthors,AuthorDetails,PostOfAuth,PublicPosts,PostOfAuthors,PostDetails,PostComments,FriendRequest

urlpatterns = [
    #Just retrieves list of authors in the database
    path('/auth/',include('knox.urls')),
    #for registering a user route
    path('auth/register',RegisterAPI.as_view(), name='signup'),

    # for logining in a user route
    path('auth/login',LoginAPI.as_view(), name='login'),

    path('auth/user',UserAPI.as_view()),

    path('auth/logout',knox_views.LogoutView.as_view(),name='knox_logout'),

    path('authors/', ListAuthors.as_view()),
    #Retrieves this specific authors details
    path('authors/<pk>/', AuthorDetails.as_view(),name='authors'),

    path('author/posts/',PostOfAuth.as_view()),


    #All posts marked as public on the server
    path('posts/',PublicPosts.as_view(), name='posts'),
    #All posts made by this specific author, visible to authenticated user
    path('author/<pk>/posts/', PostOfAuthors.as_view()),
    #Just retrieves a single post with that id
    path('posts/<pk>/',PostDetails.as_view()),
    #Just retrieves comments to that specific post
    path('posts/<pk>/comments/',PostComments.as_view()),
    #Just sends a friend request
    path('friendRequest/',views.send_friend_request),
    # result of a friend request
    path('friendResult', views.respond_to_friend_request),
    # Just un-befriend(unfollow) an author
    path('unfriend/', views.unfriend),
    # Get all my friends
    path('friends/', views.get_friends),
    # Get all my friends
    path('local_friends/', views.get_friends_local),
    # Get all my friends
    path('api/authors/<authorid>/friends/', views.get_friends),
    # Get all my friends
    path('api/local_friends/', views.get_friends_local),
    # Ask if 2 authors are friends
    path('api/author/<authorid>/friends/<authorid2>/', views.check_friendship, name='friendship')
]
