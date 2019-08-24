import os
from django.core.exceptions import ImproperlyConfigured

def get_env_var(var_name):
    try:
        return os.environ.get(var_name)
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)