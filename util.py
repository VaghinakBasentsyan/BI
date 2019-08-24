import warnings

import datetime
import fredapi
import pandas as pd
import timetools

from apps.core.utils import get_env_var

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
    u'T10YFF',
    u'BUSLOANS'
    ]

# metadata = []
#
#
# for series_id in good_columns:
#     try:
#         metadata.append(fred.get_series_info(series_id))
#     except ValueError:
#         # Series sometimes get retired from FRED
#         warnings.warn('Series {} not found on FRED API'.format(series_id))
# columns = metadata[0].keys()
#
# with open('test.csv', 'w') as f:
#     for key in columns:
#         f.write("%s," % (key))
#     f.write('\n')
#     for i in metadata:
#             for key in columns:
#                 f.write("%s," % (i[key]))
#             f.write('\n')
# print(metadata)


metadata = {}
for series_id in good_columns:
    try:
        metadata[series_id] = fred.get_series_info(series_id)
    except ValueError:
        # Series sometimes get retired from FRED
        warnings.warn('Series {} not found on FRED API'.format(series_id))

def get_series_data(series_id):
    series_data = fred.get_series_first_release(series_id)

    series_index = [ix.strftime('%Y-%m-%d') for ix in series_data.index]
    series_data.index = series_index
    return series_data

obs = {}
for series_id in metadata.keys():
    good_columns.remove(series_id)
    print(good_columns)
    series_data = get_series_data(series_id)
    obs[series_id] = series_data

monthly = [series_id for series_id
           in metadata
           if metadata[series_id]['frequency'] == 'Monthly']

all_monthly = pd.DataFrame({metadata[series_id]['title']: obs[series_id]
                            for series_id in monthly})

fin_data =all_monthly

fin_data = fin_data[fin_data.index <
                    datetime.datetime.today().strftime('%Y-%m-%d')]

fin_data.to_csv('fin_data.csv')
usrec = fred.get_series_first_release('USREC')
usrec.index = [ix.isoformat().split('T')[0] for ix in usrec.index]
bool_match = usrec.index > fin_data.first_valid_index()
target_series = usrec[bool_match]


target_name = 'US Recession in 13 Weeks'
# timetools.slide(target_series, 7 * 13)
target_frame = pd.DataFrame({target_name: target_series})
#
fin_data['month'] = fin_data.index
target_frame['month'] = target_frame.index

# modeling_frame = timetools.expand_frame_merge(fin_data, target_frame)
all_data = pd.concat([target_frame, fin_data])
all_data.to_csv('all.csv')
target_frame.to_csv('target.csv')
fin_data.to_csv('monthly.csv')
modeling_frame = fin_data

merged = pd.merge(fin_data, target_frame, on=['month', 'month'])
na_counts = modeling_frame.isnull().sum(axis=1)
earliest_useful_day = na_counts[na_counts < 20].index[0]

modeling_frame = modeling_frame[modeling_frame.index >= earliest_useful_day]

n_rows = len(modeling_frame)
validation_first_day = modeling_frame[modeling_frame.index >=
                                      '1980-01-01'].index[0]
validation_point = modeling_frame.index.get_loc(validation_first_day)
holdout_first_day = modeling_frame[modeling_frame.index >=
                                   '1995-01-01'].index[0]
holdout_point = modeling_frame.index.get_loc(holdout_first_day)

tvh = pd.Series(['T'] * n_rows)
tvh.loc[validation_point:holdout_point] = 'V'
tvh.loc[holdout_point:] = 'H'
tvh.index = modeling_frame.index

modeling_frame['TVH'] = tvh

fname = 'financials-{}.csv'.format(datetime.datetime.today().
                                   strftime('%Y-%m-%d'))
modeling_frame.to_csv(fname, index=True, index_label='Date', encoding='utf-8')

from sklearn import svm
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    fin_data.values, target_frame['US Recession in 13 Weeks'].values,
    test_size=0.33
    )
clf = svm.SVC(gamma='scale')
clf.fit(X_train, y_train)