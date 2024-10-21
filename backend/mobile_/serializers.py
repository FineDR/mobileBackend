from rest_framework import serializers
from .models import User,Message,TransactionDetails,Category 

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password']  # Ensure id is included
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            fullname=validated_data['fullname']
        )
        if 'password' not in validated_data:
            raise serializers.ValidationError({"password": "This field is required."})

        user.set_password(validated_data['password'])
        user.save()
        return user
    
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','message']  # Only include fields that are allowed to be set by the user

    def create(self, validated_data):
        # Get the user from the request context, not from validated_data
        user = self.context['request'].user
        return Message.objects.create(user=user, **validated_data)
    
class TransactionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetails
        fields = [
            'id',
            'amountReceived',
            'balanceAfterTransaction',
            'category',
            'sender',
            'transactionDate',
            'transactionId',
            'user'  # The foreign key field for the related user
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'user']  # Include user if you want it to be part of the serialized data

    def create(self, validated_data):
        return Category.objects.create(**validated_data)