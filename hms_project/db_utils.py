# hms_project/db_utils.py
import threading

# Create a thread-local storage object
_thread_locals = threading.local()

def set_tenant_db_for_router(db_name):
    """
    Set the database name for the current thread.
    The router will use this to determine which DB to use.
    """
    setattr(_thread_locals, 'db_name', db_name)

def get_tenant_db_for_router():
    """
    Get the database name for the current thread.
    """
    return getattr(_thread_locals, 'db_name', None)

def clear_tenant_db_for_router():
    """
    Clear the database name from the current thread.
    """
    if hasattr(_thread_locals, 'db_name'):
        delattr(_thread_locals, 'db_name')