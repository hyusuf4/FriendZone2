from rest_framework import serializers
from .models import Author, FriendRequest, Friends,Post,Comment,VisibleToPost,Categories
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import datetime
from django.db.models import Q




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','email','password')
        extra_kwargs={'password':{'write_only':True}}

    def create(self,validated_data):
        user=User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])
        author=Author.objects.create(userName=validated_data['username'], password=validated_data['password'],owner=user)
        return user

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self,data):
        user=authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Crendentials")


class AuthorSerializer(serializers.ModelSerializer):

    firstName=serializers.CharField(blank=True,null=True)
    class Meta:
        model = Author
        fields=('pk','firstName','lastName','userName','hostName','githubUrl')

    def update(self, instance, validated_data):
        instance.firstName = validated_data.get('firstName', instance.firstName)
        instance.lastName = validated_data.get('lastName', instance.lastName)
        instance.userName = validated_data.get('userName', instance.userName)
        instance.githubUrl = validated_data.get('githubUrl', instance.githubUrl)
        instance.save()
        return instance



class FriendRequestSerializer(serializers.ModelSerializer):
    # pk = serializers.PrimaryKeyRelatedField(queryset=FriendRequest.objects.all())
    created = serializers.DateTimeField(default=timezone.now())
    accepted = serializers.BooleanField(default=False)
    regected = serializers.BooleanField(default=False)

    class Meta:
        model=FriendRequest
        fields=('pk','from_author',
        'to_author',
        'created','accepted',
        'regected')

    def create(self, validated_data):
        new_instance = FriendRequest.objects.create(\
            from_author=validated_data.get('from_author'),\
            to_author=validated_data.get('to_author'),\
            created=timezone.now(),\
            accepted=True,\
            regected=True,\
            # test=parse_datetime(validated_data.get('test')).strftime("%Y-%m-%d %H:%M:%S")
            test=parse_datetime("2012-04-23T18:25:43.511Z").strftime("%Y-%m-%d %H:%M:%S")

        )

        new_instance.save()

        return new_instance

class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Friends
        fields=('pk','author1',
        'author2',
        'date')

class PostSerializer(serializers.ModelSerializer):
    publicationDate = serializers.DateTimeField(default=datetime.now())
    class Meta:
        model = Post
        fields = ('pk','source','origin','contentType','publicationDate', 'content', 'title', 'permission','author','unlisted')
    
    def create(self, validated_data,author):

        new_instance = Post.objects.create(content=validated_data.get('content'),title=validated_data.get('title'), permission=validated_data.get('permission'),author=author,publicationDate=datetime.now())
        if validated_data.get('categories'):
            for category in validated_data.get('categories'):
                categories=Categories.create(post=new_instance,category=category)
        if validated_data.get('permission') == 'F':
            friends=Friends.objects.filter(Q(author1=author)| Q(author2=author))
            for friend in friends:
                if friend.author1 == author:
                    new_visible=VisibleToPost.objects.create(post=new_instance,author=friend.author2)
                elif friend.author2 == author:
                    new_visible=VisibleToPost.objects.create(post=new_instance,author=friend.author1)
        elif validated_data.get('permission') == 'FH':
            friends=Friends.objects.filter(Q(author1=author)| Q(author2=author))
            for friend in friends:
                if friend.author1 == author and friend.author2.hostName == 'http://127.0.0.1:8000':
                    new_visible=VisibleToPost.objects.create(post=new_instance,author=friend.author2)
                elif friend.author2 == author and friend.author1.hostName == 'http://127.0.0.1:8000':
                    new_visible=VisibleToPost.objects.create(post=new_instance,author=friend.author1)
        elif validated_data.get('permission') == 'FF':
            friends=Friends.objects.filter(Q(author1=author)| Q(author2=author))
            foaf=set()
            for friend in friends:
                if friend.author1 == author:
                    foaf1=Friends.objects.filter(Q(author1=friend.author2)| Q(author2=friend.author2)).values('author1')
                    foaf2=Friends.objects.filter(Q(author1=friend.author2)| Q(author2=friend.author2)).values('author2')
                    if foaf1 != author:
                        foaf.add(foaf1)
                    if foaf1 != author:
                        foaf.add(foaf2)
                # elif friend.author2 == author:
                #     foaf1=Friends.objects.filter(Q(author1=friend.author2)| Q(author2=friend.author2)).values('author1')
                #     foaf2=Friends.objects.filter(Q(author1=friend.author2)| Q(author2=friend.author2)).values('author2')
                #     if foaf1 != author:
                #         foaf.add(foaf1)
                #     if foaf1 != author:
                #         foaf.add(foaf2)
            print(foaf)
            
        return new_instance


class VisibleToPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=VisibleToPost
        fields=('post','author')
     
    def get_visible(post):
        self.object.filter(post=post)
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Comment
        fields=('pk','comment','author','postid','published','content-type')


class Categories(serializers.ModelSerializer):
    model=Categories
    fields=('post','category')


# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Image
#         fields=('pk','post_id','img')
