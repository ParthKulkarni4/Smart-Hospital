# hms_project/middleware.py
from .db_utils import set_tenant_db_for_router, clear_tenant_db_for_router
from django.conf import settings

class TenantDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Default to 'default' database if user is not authenticated
        db_name = 'default' 
        
        # Check if the user is authenticated and is not a SuperAdmin
        # SuperAdmins will use the 'default' DB
        if request.user.is_authenticated and request.user.role != 'SuperAdmin':
            # Get the 'admin_owner' field from our Custom User model
            db_name = request.user.admin_owner

            # Check if this database is actually defined in settings
            if db_name not in settings.DATABASES:
                # Log an error or raise an exception
                # For now, fall back to default
                print(f"Warning: Database '{db_name}' not found in settings. Falling back to default.")
                db_name = 'default'

        # Set the database name in thread-local storage
        set_tenant_db_for_router(db_name)

        # Process the request
        response = self.get_response(request)

        # Clear the database name from thread-local storage after the request
        clear_tenant_db_for_router()

        return response