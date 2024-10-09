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
    path('login/',UserLogin.as_view()),
    path('logout/',UserLogout.as_view()),
    path('category/', CategoryViewList.as_view()),
    path('category/<int:pk>/', CategoryViewDetails.as_view()),

    path('transaction/', TransactionViewList.as_view()),
    path('transaction/<int:pk>/', TransactionViewDetails.as_view()),

    path('messages/', MessageViewList.as_view()),
    path('messages/<int:pk>/', MessageViewDetails.as_view()),
]
