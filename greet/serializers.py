from rest_framework import serializers
from django.contrib.auth import get_user_model

User=get_user_model()

from rest_framework import serializers

from rest_framework import serializers
from django.contrib.auth import authenticate

from rest_framework import serializers
from django.contrib.auth import authenticate

# serializers.py
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()




class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        password2 = validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords do not match'})

        user_obj = User.objects.create_user(username=username, email=email, password=password)
        return user_obj
    
class UserDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['username','email','first_name','last_name']

# serializers.py

from rest_framework import serializers
from .models import Show, Booking

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['id', 'title', 'movie', 'time', 'date', 'capacity', 'is_active','language','type', 'ticket_price','description','image']

from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    show_title = serializers.SerializerMethodField()  # Add a SerializerMethodField for movie title

    class Meta:
        model = Booking
        fields = [ 'id','show_title', 'show', 'number_of_tickets', 'total_amount', ]  # Include 'movie_title' in the fields

    def get_show_title(self, obj):
        return obj.show.title

# serializers.py

from rest_framework import serializers
from .models import Show

class ShowSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['title', 'ticket_price', 'image','description','time','date']

from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

