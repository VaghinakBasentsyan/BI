import warnings
import datetime
import fredapi
import pandas as pd
from django.conf import settings
from datetime import datetime
from django.conf import settings

from .models import Report
from .svm_model import add_predict


fred = fredapi.Fred(api_key='14d8dd169b3688444536eadb2edf0896')

good_columns = [
    u'AWHAETP',
    u'ACDGNO',
    u'M06006USM156NNBR',
    u'NEWORDER',
    u'PERMIT',
    u'SP500',
    u'M2',
    u'UEMPMEAN',
    # u'T10YFF',
    # u'BUSLOANS'
    ]


def get_series_data(series_id):
    series_data = fred.get_series_first_release(series_id)

    series_index = [ix.strftime('%Y-%m-%d') for ix in series_data.index]
    series_data.index = series_index

    return series_data


def collect_data():
    metadata = {}
    for series_id in good_columns:
        try:
            metadata[series_id] = fred.get_series_info(series_id)
        except ValueError:
            # Series sometimes get retired from FRED
            warnings.warn('Series {} not found on FRED API'.format(series_id))
    obs = {}
    for series_id in metadata.keys():
        good_columns.remove(series_id)
        series_data = get_series_data(series_id)
        obs[series_id] = series_data

    monthly = [series_id for series_id
               in metadata
               if metadata[series_id]['frequency'] == 'Monthly']

    all_monthly = pd.DataFrame({metadata[series_id]['title']: obs[series_id]
                                for series_id in monthly})

    monthly_data =all_monthly

    monthly_data = monthly_data[monthly_data.index <
                        datetime.today().strftime('%Y-%m-%d')]

    monthly_data.to_csv('fin_data.csv')
    usrec = fred.get_series_first_release('USREC')
    usrec.index = [ix.isoformat().split('T')[0] for ix in usrec.index]
    bool_match = usrec.index > monthly_data.first_valid_index()
    target_series = usrec[bool_match]

    target_name = 'recession'
    # timetools.slide(target_series, 7 * 13)
    target_frame = pd.DataFrame({target_name: target_series})

    monthly_data.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
    target_frame.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
    monthly_data['date'] = monthly_data.index
    target_frame['date'] = target_frame.index
    #
    # monthly_data['date'] = pd.to_datetime(monthly_data['date'])
    # monthly_data['date'] = (monthly_data['date'] - monthly_data['date'].min()) / np.timedelta64(1, 'D')
    # target_frame['date'] = pd.to_datetime(target_frame['date'])
    # target_frame['date'] = (target_frame['date'] - target_frame['date'].min()) / np.timedelta64(1, 'D')

    all_data = pd.merge(target_frame, monthly_data, on=['date'])
    final_df = add_predict(all_data)

    file_name = "{}financials-{}.csv".format(
        settings.MEDIA_ROOT,
        format(datetime.today().strftime('%Y-%m-%d'))
    )
    final_df.to_csv(file_name)

    report = Report()
    report.file_path = file_name
    report.save()


if __name__ == "__main__":
    collect_data()