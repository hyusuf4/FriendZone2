from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .api import RegisterAPI,LoginAPI,UserAPI
from knox import views as knox_views


urlpatterns = [
    #Just retrieves list of authors in the database
    path('api/auth',include('knox.urls')),
    #for registering a user route
    path('api/auth/register',RegisterAPI.as_view()),

    # for logining in a user route
    path('api/auth/login',LoginAPI.as_view()),

    path('api/auth/user',UserAPI.as_view()),

    path('api/auth/logout',knox_views.LogoutView.as_view(),name='knox_logout'),

    path('api/authors/', views.authors_list),
    #Retrieves this specific authors details
    path('api/authors/<pk>', views.author_details),

    path('api/author/posts',views.post_visibleToAuth),


    #All posts marked as public on the server
    path('api/posts/',views.public_posts),
    #All posts made by this specific author, visible to authenticated user
    path('api/author/<pk>/posts', views.author_post),
    #Just retrieves a single post with that id
    path('api/posts/<pk>',views.post_details),
    #Just retrieves comments to that specific post
    path('api/posts/<pk>/comments',views.post_comments),
    #Just sends a friend request
    path('api/friendRequest',views.friend_request),
    # result of a friend request
    path('api/friendResult', views.friend_result),
    # Just un-befriend(unfollow) an author
    path('api/unfriend', views.unfriend)
]

urlpatterns = format_suffix_patterns(urlpatterns)
