from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .api import RegisterAPI,LoginAPI,UserAPI
from knox import views as knox_views
from .views import ListAuthors,AuthorDetails,PostOfAuth,PublicPosts,PostOfAuthors,PostDetails,PostComments,FriendRequest


urlpatterns = [
    #Just retrieves list of authors in the database
    path('api/auth',include('knox.urls')),
    #for registering a user route
    path('api/auth/register',RegisterAPI.as_view()),

    # for logining in a user route
    path('api/auth/login',LoginAPI.as_view()),

    path('api/auth/user',UserAPI.as_view()),

    path('api/auth/logout',knox_views.LogoutView.as_view(),name='knox_logout'),

    path('api/authors', ListAuthors.as_view()),
    #Retrieves this specific authors details
    path('api/authors/<pk>', AuthorDetails.as_view(),name='authors'),

    path('api/author/posts',PostOfAuth.as_view()),


    #All posts marked as public on the server
    path('api/posts',PublicPosts.as_view()),
    #All posts made by this specific author, visible to authenticated user
    path('api/author/<pk>/posts', PostOfAuthors.as_view()),
    #Just retrieves a single post with that id
    path('api/posts/<pk>',PostDetails.as_view()),
    #Just retrieves comments to that specific post
    path('api/posts/<pk>/comments',PostComments.as_view()),
    #Just sends a friend request
    path('api/friendRequest',views.send_friend_request),
    # result of a friend request
    path('api/friendResult', views.respond_to_friend_request),
    # Just un-befriend(unfollow) an author
    path('api/unfriend', views.unfriend),
    # Get all my friends
    path('api/friends', views.get_friends),
    # Get all my friends
    path('api/local_friends', views.get_friends_local)

]

urlpatterns = format_suffix_patterns(urlpatterns)
