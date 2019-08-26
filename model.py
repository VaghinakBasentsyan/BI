from sklearn.svm import SVC
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from statsmodels.tsa.arima_model import ARIMA


def create_model(*args, **kwargs):
    return SVC(gamma='scale', probability=True, kernel='rbf')

monthly_data = pd.read_csv('fin_data.csv')
target = pd.read_csv('target.csv')

monthly_data = monthly_data.iloc[1:]

monthly_data.replace([np.inf, -np.inf], np.nan)
target.replace([np.inf, -np.inf], np.nan)

monthly_data.fillna(0)
target.fillna(0)



# monthly_data['date'] = pd.to_datetime(monthly_data['date'])
# monthly_data['date'] = (monthly_data['date'] - monthly_data['date'].min()) / np.timedelta64(1,'D')
# target['date'] = pd.to_datetime(target['date'])
# target['date'] = (target['date'] - target['date'].min()) / np.timedelta64(1,'D')


if __name__ == "__main__":

    X_train, X_test, y_train, y_test = train_test_split(
        monthly_data.values, target['US Recession in 13 Weeks'].values,
        test_size=0.33
        )
    X_train = np.nan_to_num(X_train)
    X_test = np.nan_to_num(X_test)

    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
                         'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
                        {'kernel': ['sigmoid'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
                         'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]},
                        {'kernel': ['linear'], 'C': [0.001, 0.10, 0.1, 10, 25, 50, 100, 1000]}
                        ]

    clf = SVC(C=10, kernel='rbf', gamma=1e-05, probability=True)

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    # clf.predict()
    print(accuracy_score(y_test, y_pred))

    from statsmodels.tsa.vector_ar.var_model import VAR
    from random import random
    # contrived dataset with dependency

    model = VAR(X_train)
    model_fit = model.fit()
    yhat = model_fit.forecast(model_fit.y, steps=1)
    print(yhat)
    print(clf.predict(yhat))
    # print(y_train)