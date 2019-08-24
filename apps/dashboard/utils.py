from fredapi import Fred
from apps.core.utils import get_env_var


import datetime

import matplotlib as plt
def data_collector():
    fred = Fred(api_key=get_env_var('ACCESS_KEY'))
    data = fred.get_series('SP500')

def plot_date_data(dataframe, column_names):
    x_axis = [datetime.datetime.strptime(x, '%Y-%m-%d')
              for x in dataframe.index]
    import matplotlib.dates as mdates
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    years_fmt = mdates.DateFormatter('%Y')
    fig, ax = plt.subplots()

    for column_name in column_names:
        data = dataframe[column_name]
        ax.plot(x_axis, data)
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)
    ax.xaxis.set_minor_locator(months)
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.grid(True)
    fig.autofmt_xdate()


plot_date_data(plot_data[plot_data.index > '2000-01-01'],
               ['pred_{}'.format(i) for i in range(10)])