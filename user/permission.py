from rest_framework.permissions import BasePermission

class isBannedUser(BasePermission):
    message = "Your account has been banned."

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if user is None:
            return True  # Allow if no user
        if not getattr(user, 'is_authenticated', False):
            return True  # Allow unauthenticated users (AnonymousUser)
        return not getattr(user, 'is_banned', False)  # Block only banned authenticated users

class IsAdminUser(BasePermission):
    message = "You must be an admin user to access this resource."

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if user is None:
            return False
        return user.is_authenticated and user.role == 'ADMIN'