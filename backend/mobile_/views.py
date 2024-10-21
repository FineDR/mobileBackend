from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User,Message,TransactionDetails,Category
from .serializers import UserSerializer,MessageSerializer,CategorySerializer,TransactionDetailsSerializer
from rest_framework.views import APIView
from rest_framework.views import Response,status
from rest_framework import permissions
from django.http import Http404
from rest_framework import permissions
from rest_framework.exceptions import NotFound
import logging

# Create your views here.

class UserViews(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(email=request.data['email']).exists():
                return Response({'error':'the email exists'},status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        user=User.objects.all()
        serializer=UserSerializer(user,many=True)
        return Response(serializer.data)
    

class UserViewDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object_by_user_id(self, user_id):
        try:
            return User.objects.get(user_id=user_id)  # Look up by user_id
        except User.DoesNotExist:
            raise Http404("User not found by user_id.")

    def get_object_by_pk(self, pk):
        try:
            return User.objects.get(pk=pk)  # Look up by pk
        except User.DoesNotExist:
            raise Http404("User not found by pk.")

    def get(self, request, user_id=None, pk=None, format=None):
        if user_id is not None:
            user = self.get_object_by_user_id(user_id)
        elif pk is not None:
            user = self.get_object_by_pk(pk)
        else:
            raise Http404("No valid identifier provided.")
        
        serializer = UserSerializer(user)

        # Log user details to the console
        logger.info(f"Retrieved user details: {serializer.data}")

        return Response(serializer.data)

    def put(self, request, user_id=None, pk=None, format=None):
        if user_id is not None:
            user = self.get_object_by_user_id(user_id)
        elif pk is not None:
            user = self.get_object_by_pk(pk)
        else:
            raise Http404("No valid identifier provided.")
        
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Log updated user details to the console
            logger.info(f"Updated user details: {serializer.data}")

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id=None, pk=None, format=None):
        if user_id is not None:
            user = self.get_object_by_user_id(user_id)
        elif pk is not None:
            user = self.get_object_by_pk(pk)
        else:
            raise Http404("No valid identifier provided.")
        
        user.delete()

        # Log deletion of the user
        logger.info(f"Deleted user: {user.user_id}")  # Assuming user_id is a field in your User model

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user using email and password
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            
            # Prepare the response data
            response_data = {
                'token': token.key,
                'email': UserSerializer(user).data['email'],
                'id': user.id  # Return the user's ID
            }
            
            # Log the successful login response
            print("Login successful:", response_data)
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Log the error response
            error_response = {'error': 'Invalid email or password'}
            print("Login failed:", error_response)
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
class UserLogout(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request):
        try:
            token=request.auth
            if token is not None:
                token.delete()
                return Response({'messages':'logout successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'error':'No active session found'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
MessageView.........................
"""

class MessageViewList(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated
    def post(self, request):
            request.data['user'] = request.user.id

            # Pass the request context to the serializer
            serializer = MessageSerializer(data=request.data, context={'request': request})
            
            if serializer.is_valid():
                message = serializer.save()
                return Response({'id': message.id, 'message': message.message}, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    

class MessageViewDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id=None, pk=None, format=None):
        if pk is not None:
            # Fetch a specific message by primary key for the authenticated user
            try:
                message = Message.objects.get(pk=pk, user_id=user_id)  # Ensure user_id is used to check ownership
                serializer = MessageSerializer(message)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Message.DoesNotExist:
                return Response({"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if user_id is not None:
            # If no pk is provided, fetch all messages for the given user_id
            messages = Message.objects.filter(user_id=user_id)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Primary key or User ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk, format=None):
        # Update a message by primary key for the authenticated user
        try:
            message = Message.objects.get(pk=pk, user_id=request.user.id)
            serializer = MessageSerializer(message, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Updated successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Message.DoesNotExist:
            return Response({"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        # Delete a message by primary key for the authenticated user
        try:
            message = Message.objects.get(pk=pk, user_id=request.user.id)
            message.delete()
            return Response({'message': 'The item deleted successfully.'}, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            return Response({"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

logger = logging.getLogger(__name__)

class CategoryViewList(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request):
        # Add the user ID from the request user
        data = request.data.copy()  # Create a mutable copy
        data['user'] = request.user.id  # Add the logged-in user's ID
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            category = serializer.save()  # Save the category instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        logger.debug(f"User: {request.user} requesting categories.")

        # Check if the user is authenticated (again permission_classes will enforce this)
        if not request.user.is_authenticated:
            logger.warning(f"Unauthenticated access attempt by user: {request.user}")
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        # Fetch all categories
        categories = Category.objects.all()

        # Serialize the category list
        serializer = CategorySerializer(categories, many=True)

        # Log the retrieved categories for debugging purposes
        logger.debug(f"Categories retrieved: {serializer.data}")

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CategoryViewDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id=None, pk=None, format=None):
        if user_id is not None:
            # Fetch categories based on user ID (foreign key)
            categories = Category.objects.filter(user__id=user_id)  # Assuming 'user' is the foreign key in Category
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if pk is not None:
            # Fetch a specific category by primary key
            try:
                category = Category.objects.get(pk=pk)
                serializer = CategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "User ID or PK must be provided."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        # Update a category by primary key
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'The data or item updated successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        # Delete a category by primary key
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({'message': 'The item deleted successfully'}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        

class TransactionViewList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Add the user ID to the request data
        request.data['user'] = request.user.id
        
        # Check if a transaction with the same transactionId already exists
        transaction_id = request.data.get('transactionId')
        if TransactionDetails.objects.filter(transactionId=transaction_id, user=request.user).exists():
            return Response({'error': 'Transaction with this ID already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the request data
        serializer = TransactionDetailsSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Use HTTP_201_CREATED for successful creation
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        transaction=TransactionDetails.objects.all()
        serializer=TransactionDetailsSerializer(transaction,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class TransactionViewDetails(APIView):
    # Handle fetching object based on user_id and pk
    def get_object_by_user_id(self, user_id):
        try:
            # Get all transactions for the specific user
            return TransactionDetails.objects.filter(user_id=user_id)
        except TransactionDetails.DoesNotExist:
            raise Http404

    def get_object_by_pk(self, pk):
        try:
            # Get transaction by primary key (pk)
            return TransactionDetails.objects.get(pk=pk)
        except TransactionDetails.DoesNotExist:
            raise Http404

    # Get method for handling requests with both user_id and pk
    def get(self, request, user_id=None, pk=None, format=None):
        if user_id and pk:
            transaction = self.get_object_by_user_id(user_id).filter(pk=pk).first()
            if not transaction:
                raise Http404
            serializer = TransactionDetailsSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user_id:
            transactions = self.get_object_by_user_id(user_id)
            serializer = TransactionDetailsSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif pk:
            transaction = self.get_object_by_pk(pk)
            serializer = TransactionDetailsSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No user_id or pk provided"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id=None, pk=None, format=None):
        if user_id and pk:
            transaction = self.get_object_by_user_id(user_id).filter(pk=pk).first()
            if not transaction:
                raise Http404
            serializer = TransactionDetailsSerializer(transaction, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Item updated successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "No user_id or pk provided for update"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id=None, pk=None, format=None):
        if user_id and pk:
            transaction = self.get_object_by_user_id(user_id).filter(pk=pk).first()
            if not transaction:
                raise Http404
            transaction.delete()
            return Response({'message': 'Item deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No user_id or pk provided for deletion"}, status=status.HTTP_400_BAD_REQUEST)
