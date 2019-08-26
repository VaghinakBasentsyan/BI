from fredapi import Fred
from apps.core.utils import get_env_var


import datetime

import matplotlib as plt

def data_collector():
    fred = Fred(api_key=get_env_var('ACCESS_KEY'))
    data = fred.get_series('SP500')
