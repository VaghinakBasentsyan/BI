from sklearn.svm import SVC
import pandas as pd
import datetime
import numpy as np
from sklearn.model_selection import train_test_split
from statsmodels.tsa.vector_ar.var_model import VAR


def create_model(*argsall_frame, **kwargs):
    return SVC(gamma='scale', probability=True, kernel='rbf')


def add_predict(df):
    all_frame = df.replace([np.inf, -np.inf], np.nan).fillna(0)

    all_frame['date'] = pd.to_datetime(all_frame['date']).astype(int) / 10**9
    target = df['recession'].values.tolist()

    monthly_data = all_frame.drop(['recession'], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        monthly_data.values, target,
        test_size=0.33
    )
    X_train = np.nan_to_num(X_train)
    X_test = np.nan_to_num(X_test)
    #
    # tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
    #                      'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
    #                     {'kernel': ['sigmoid'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
    #                      'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
    #                     {'kernel': ['linear'], 'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]}
    #                     ]

    clf = SVC(C=10, kernel='rbf', gamma=1e-05, probability=True)

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    forecast_data = df.drop(['recession', 'date'], axis=1)
    forecast_data = forecast_data.replace([np.inf, -np.inf], np.nan).fillna(0)
    forecast_data = forecast_data.values

    forecast_data = np.nan_to_num(forecast_data)
    model = VAR(forecast_data)
    model_fit = model.fit()
    yhat = model_fit.forecast(model_fit.y, steps=1)

    yhat = list(yhat[0])
    yhat.insert(
        0,
        (
                pd.DataFrame({'time': [pd.to_datetime(datetime.datetime.today().strftime('%Y-%m-%d'))]}).astype(int)
                / 10**9
        ).values[0][0]
    )

    prediction = clf.predict([yhat])[0]
    yhat[0] = datetime.datetime.today().strftime('%Y-%m-%d')
    yhat.insert(0, prediction)
    df.append(pd.Series(yhat, index=all_frame.columns), ignore_index=True)
    # df['date'] = pd.to_datetime(df['date']).astype(int) / 10 ** 9
    return df

