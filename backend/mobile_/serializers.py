from rest_framework import serializers
from .models import User,Message,TransactionDetails,Category  # Update the import to reference the new User model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Use the renamed User model
        fields = ['fullname', 'email', 'password']  # Define the fields to be serialized
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only

    def create(self, validated_data):
        # Create a new user instance with the validated data
        user = User(
            email=validated_data['email'],
            fullname=validated_data['fullname']
        )
        # Set the password securely
        user.set_password(validated_data['password'])
        # Save the user instance
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message']  # Only include fields that are allowed to be set by the user

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
        fields = ['category_id', 'category_name', 'user'] 