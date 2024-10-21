from django.urls import path
from .views import(
    UserViews,
    UserViewDetails,
    UserLogin,
    UserLogout,
    CategoryViewList,
    CategoryViewDetails,
    MessageViewList,
    MessageViewDetails,
    TransactionViewList,
    TransactionViewDetails
)

urlpatterns = [
    path('user/',UserViews.as_view()),
    path('user/<int:pk>/',UserViewDetails.as_view()),
    path('user/<int:user_id>/',UserViewDetails.as_view()),
    path('login/',UserLogin.as_view()),
    path('logout/',UserLogout.as_view()),
    path('category/', CategoryViewList.as_view()),
    path('category/<int:pk>/', CategoryViewDetails.as_view()),
    path('category/user/<int:user_id>/', CategoryViewDetails.as_view(), name='user-categories'),  # Fetch by user ID
    path('transaction/', TransactionViewList.as_view()),
    path('transaction/user/<int:user_id>/', TransactionViewDetails.as_view()),
    path('transaction/<int:user_id>/<int:pk>/', TransactionViewDetails.as_view()),
    
    # URL pattern to handle only user_id
    path('transaction/<int:user_id>/', TransactionViewDetails.as_view(), name='transactions-by-user'),
    path('messages/', MessageViewList.as_view()),
    path('messages/user/<int:user_id>/', MessageViewDetails.as_view()),
    path('messages/<int:pk>/', MessageViewDetails.as_view()),
]
