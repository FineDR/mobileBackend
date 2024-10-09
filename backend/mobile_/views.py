from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User,Message,TransactionDetails,Category
from .serializers import UserSerializer,MessageSerializer,CategorySerializer,TransactionDetailsSerializer
from rest_framework.views import APIView
from rest_framework.views import Response,status
from rest_framework import permissions
from django.http import Http404
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
    def get_object(self,pk):
        try:
            return self.User.objects.get(pk)
        except User.DoesNotExist:
            raise Http404
        
    def get(self,request,pk,format=None):
        user=self.get_object(pk)
        serializer=UserSerializer(user)
        return Response(serializer.data)
    
    def put(self,request,pk,format=None):
        user=self.get_object(pk)
        serializer=UserSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None):
        user=self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserLogin(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self,request):
        email=request.data['email']
        password=request.data['password']

        user=authenticate(request,email=email,password=password)
        if user is not None:
            token,created=Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token':token.key,
                    'user':UserSerializer(user).data
                },status=status.HTTP_200_OK
            )
        else:
            return Response({'error':'user not found'},status=status.HTTP_400_BAD_REQUEST)

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
    def get_object(self,pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404
    
    def get(self,request,pk,format=None):
        message=self.get_object(pk)
        serializer=MessageSerializer(message)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk,format=None):
        message=self.get_object(pk)
        serializer=MessageSerializer(message,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Updated successfully'},status=status.HTTP_200_OK)
        return Response({'error':'failed because of serializer rules'},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None):
        message=self.get_object(pk)
        message.delete()
        return Response({'message':'you delete and item'},status=status.HTTP_200_OK)
    

class CategoryViewList(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request):
        request.data['user'] = request.user.id
        serializer=CategorySerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        category=Category.objects.all()
        serializer=CategorySerializer(category,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class CategoryViewDetails(APIView):

    def get_object(self,pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404
        
    def get(self,request,pk,format=None):
        category=self.get_object(pk)
        serializer=CategorySerializer(category)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk,format=None):
        category=self.get_object(pk)
        serializer=CategorySerializer(category,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'the data or item updated successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None):
        category=self.get_object(pk)
        category.delete()
        return Response({'message':'the item deleted successfully'},status=status.HTTP_200_OK)
    


class TransactionViewList(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request):
        request.data['user']=request.user.id
        serializer=TransactionDetailsSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        transaction=TransactionDetails.objects.all()
        serializer=TransactionDetailsSerializer(transaction,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class TransactionViewDetails(APIView):
    def get_object(self,pk):
        try:
            return TransactionDetails.objects.get(pk=pk)
        except TransactionDetails.DoesNotExist:
            raise Http404
        
    def get(self,request,pk,format=None):
        transaction=self.get_object(pk)
        serilizer=TransactionDetailsSerializer(transaction)
        return Response(serilizer.data,status=status.HTTP_200_OK)
    def put(self,request,pk,format=None):
        transaction=self.get_object(pk)
        serializer=TransactionDetailsSerializer(transaction,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'the item updated successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        transaction=self.get_object(pk)
        transaction.delete()
        return Response({'mesassa':'the item delete successfully'},status=status.HTTP_200_OK)