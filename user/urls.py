
from django.urls import path
from .views import ProfileView, BanUser, UsersListView

urlpatterns = [
    path('users/profile/', ProfileView.as_view(), name='profile'),
    path('users/<int:pk>/', BanUser.as_view(), name='ban_user'),
    path('users/', UsersListView.as_view(), name='all_users'),

]

