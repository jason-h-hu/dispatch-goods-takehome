from ..models import UserModel
from django.views.generic import DetailView
from rest_framework import serializers
from rest_framework import generics

class UserView(DetailView):
    model = UserModel
    template_name = 'user.html'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'first_name',
            'last_name',
            'age',
            'address',
        ]

class UserAPIView(generics.ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
