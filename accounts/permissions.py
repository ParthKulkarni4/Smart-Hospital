from rest_framework.permissions import BasePermission

def has_role(user, role_name):
    """
    Check if the user has the specified role.
    """
    return user.role == role_name

class IsReceptionistOrAdmin(BasePermission):
    """
    Custom permission to only allow receptionists or admins to access.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in ['Receptionist', 'Admin']
