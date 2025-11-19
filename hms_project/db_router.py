# hms_project/db_router.py
from .db_utils import get_tenant_db_for_router

class TenantDatabaseRouter:
    """
    A router to control all database operations on models in the
    tenant-specific applications.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read tenant_apps models go to the tenant's database.
        """
        if model._meta.app_label in self.get_tenant_apps():
            return self.get_tenant_db()
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write tenant_apps models go to the tenant's database.
        """
        if model._meta.app_label in self.get_tenant_apps():
            return self.get_tenant_db()
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in a tenant_app is involved.
        This ensures that a 'Patient' (tenant) can't link to a
        'User' (shared) in a different database, *except* for the 'default' one.
        """
        # If one of the models is a shared app, allow relation
        if obj1._meta.app_label in self.get_shared_apps() or \
           obj2._meta.app_label in self.get_shared_apps():
            return True
            
        # If both models are tenant apps, they must be in the same tenant DB
        if obj1._meta.app_label in self.get_tenant_apps() and \
           obj2._meta.app_label in self.get_tenant_apps():
            return self.get_tenant_db() == self.get_tenant_db() # Should always be True if set
            
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the tenant_apps only appear in the tenant's database
        and shared_apps only appear in the 'default' (shared) database.
        """
        if db == 'default':
            # If 'db' is 'default', only allow migration if 'app_label' is a SHARED app
            return app_label in self.get_shared_apps()
        else:
            # If 'db' is NOT 'default' (e.g., 'hospital_a'), 
            # only allow migration if 'app_label' is a TENANT app
            return app_label in self.get_tenant_apps()

    def get_tenant_db(self):
        """Get the tenant DB name from thread-local storage."""
        return get_tenant_db_for_router() or 'default'

    def get_tenant_apps(self):
        """Get the list of tenant apps from settings."""
        from django.conf import settings
        return settings.TENANT_APPS

    def get_shared_apps(self):
        """Get the list of shared apps from settings."""
        from django.conf import settings
        return settings.SHARED_APPS