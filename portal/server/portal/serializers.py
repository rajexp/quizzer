from django.contrib.auth.models import User
from rest_framework import serializers
 
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'first_name', 'last_name', 'email', 'username')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)
 
    def create(self, validated_data):
        user = User(email=validated_data['email'], 
        username=validated_data['username'],
        first_name=validated_data.get('first_name'),
        last_name=validated_data.get('last_name'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.username=validated_data.get('username',instance.username)
        instance.first_name=validated_data.get('first_name',instance.first_name)
        instance.last_name=validated_data.get('last_name',instance.last_name)
        instance.set_password(validated_data.get('password',instance.password))
        instance.save()
        return instance
