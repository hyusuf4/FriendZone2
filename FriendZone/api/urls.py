from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    #Just retrieves list of authors in the database
    path('api/authors/', views.authors_list),
    #Retrieves this specific authors details
    path('api/authors/<pk>', views.author_details),
    #All posts marked as public on the server
    path('api/posts',views.public_posts),
    #All posts made by this specific author, visible to authenticated user
    path('api/author/<pk>/posts', views.author_post),
    #Just retrieves a single post with that id
    path('api/posts/<pk>',views.post_details),
    #Just retrieves comments to that specific post
    path('api/posts/<pk>/comments',views.post_comments),
    #Just sends a friend request  
    path('api/friendRequest',views.friend_request)

    
]

urlpatterns = format_suffix_patterns(urlpatterns)