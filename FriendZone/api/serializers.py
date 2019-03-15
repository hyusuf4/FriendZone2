from rest_framework import serializers
from .models import Author, FriendRequest, Friends,Post,Comment, Following
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.dateparse import parse_datetime



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
    def create(self, validated_data):
        # print(111, validated_data, 222)
        new_instance = Friends.objects.create(\
            author1=validated_data.get('to_author'),\
            author2=validated_data.get('from_author'),\
            date=timezone.now()
        )

        new_instance.save()

        return new_instance

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('pk','source','origin','content-type','publicationDate', 'content', 'title', 'permission','permitted_authors','author','unlisted')



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Comment
        fields=('pk','comment','author','postid','published','content-type')

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ('follower', 'following', 'created')

    def create(self, validated_data):
        new_instance = Following.objects.create(\
            follower=validated_data.get("requester_id"),\
            following=validated_data.get("requestee_id"),\
            created=timezone.now()\
        )
        new_instance.save()

        return new_instance


# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Image
#         fields=('pk','post_id','img')
