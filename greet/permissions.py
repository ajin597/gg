from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow administrators to create, update, or delete movie shows.
    """

    def has_permission(self, request, view):
        # Allow read-only permissions for non-administrators
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow write permissions only for administrators
        return request.user and request.user.is_staff
