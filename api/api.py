from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer,LoginSerializer
from .models import Author
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from rest_framework import status

class RegisterAPI(generics.GenericAPIView):
    serializer_class=RegisterSerializer

    def post(self,request,*args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
##        self.set_new_user_inactive(user)
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":AuthToken.objects.create(user),
            "isActive":user.is_active
        })
#     @receiver(pre_save, sender=User)
#     def set_new_user_inactive(sender, instance, **kwargs):
#         if instance._state.adding is True:
#             print("Creating Inactive User")
#             instance.is_active = False
#         else:
#             print("Updating User Record")
class LoginAPI(generics.GenericAPIView):
    serializer_class=LoginSerializer

    def post(self,request,*args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":AuthToken.objects.create(user),
            "isActive":user.is_active
        })

class UserAPI(generics.RetrieveAPIView):
    permissions_classes=[
        permissions.IsAuthenticated,
    ]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user
