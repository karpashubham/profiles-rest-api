from rest_framework import serializers

from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIViews"""
    name = serializers.CharField(max_length=10)
    
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    
    class Meta:
        """Sets up our serializer to point to our user profile model"""
        model = models.UserProfile
        fields  =('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password':{
                'write_only': True, # so that when we use get we wont see the password field included in our response
                'style':{'input_type':'password'} # so password is not visible when typing
            }
        }
    
    def create(self, validated_data):
        """Creata and return a new user"""
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )
        return user
    
    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'passowrd' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password) #saves password using a hash
        return super().update(instance, validated_data)