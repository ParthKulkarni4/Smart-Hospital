from rest_framework import permissions

def in_group(user, group_name):
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()

class CanManageTests(permissions.BasePermission):
    """
    Manage radiology tests: allowed for staff/superusers and users in group 'Radiologist' or 'Admin'.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return bool(user and (user.is_staff or user.is_superuser or in_group(user, "Admin") or in_group(user, "Radiologist")))

class CanUploadRecords(permissions.BasePermission):
    """
    Allow Radiographers and Radiologists (and Admin/staff) to create/upload records.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser or in_group(user, "Admin"):
            return True
        if in_group(user, "Radiologist") or in_group(user, "Radiographer"):
            return True
        # others read-only
        return False

class CanCreateReport(permissions.BasePermission):
    """
    Radiographers can create report drafts; Radiologists/Admin can create and finalize.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser or in_group(user, "Admin"):
            return True
        if in_group(user, "Radiologist"):
            return True
        if in_group(user, "Radiographer"):
            # allow creation of drafts
            if request.method == "POST":
                return True
            # allow editing own drafts handled in object permission
            return False
        return False

class ReportObjectPermission(permissions.BasePermission):
    """
    Object-level rules:
    - Admin/staff OR Radiologist: can edit any report (including finalize)
    - Radiographer: can edit own reports while status == 'draft'
    - Creator: can edit own draft
    - Others: read-only
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser or in_group(user, "Admin"):
            return True
        if in_group(user, "Radiologist"):
            return True
        creator = getattr(obj, "created_by", None)
        status = getattr(obj, "status", None)
        if creator and creator == user and status == "draft":
            return True
        # radiographer cannot finalize (finalize action is also guarded)
        return False
