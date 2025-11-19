# bloodbank/permissions.py
from rest_framework import permissions

class IsBloodBankStaff(permissions.BasePermission):
    """
    Allow access only to users in the 'bloodbank_staff' group or superusers.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        # adjust group name as per your project
        return user.groups.filter(name='bloodbank_staff').exists()
