from rest_framework import serializers
from .models import Author, FriendRequest, Friends,Post,Comment
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



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
    class Meta:
        model=FriendRequest
        fields=('pk','from_author',
        'to_author',
        'created','accepted',
        'regected')

class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Friends
        fields=('pk','author1',
        'author2',
        'date')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post 
        fields = ('pk','source','origin','contentType','publicationDate', 'content', 'title', 'permission','permitted_authors','author','unlisted')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Comment
        fields=('pk','comment','author','postid','published','content-type')


# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Image
#         fields=('pk','post_id','img')



