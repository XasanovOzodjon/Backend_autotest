from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSerializer, ProfileUpdateSerializer, Get_all_Users_Serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import check_password
from .permission import isBannedUser, IsAdminUser
from account.models import CustomUser


class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, isBannedUser]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user = request.user
        # To update avatar, send the request as multipart/form-data with the 'avatar' field containing the image file.
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            # If password change is requested, verify the current password
            current_password = request.data.get('password')
            new_password = request.data.get('new_password')
            confirm_new_password = request.data.get('confirm_new_password')

            if new_password or confirm_new_password:
                if not current_password or not check_password(current_password, user.password):
                    return Response({"detail": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
                if new_password != confirm_new_password:
                    return Response({"detail": "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
                user.set_password(new_password)

            serializer.save()  # This will update avatar if provided
            return Response(serializer.data, status=status.HTTP_200_OK)

class BanUser(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user.is_banned = True
        user.save()
        return Response({"detail": "User has been banned."}, status=status.HTTP_200_OK)
    
class UsersListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = CustomUser.objects.all().order_by('id')
        serializer = Get_all_Users_Serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)