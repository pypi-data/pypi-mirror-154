from sklearn.model_selection import train_test_split
import numpy as np
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor


def rfregression(data, target_column, test_size):
    """
    It does the simple regression and returns different validation metrics sores and actual data with predicted data
    data: dataset
    target_column: output variable for example of huse pricing the price column is o/p variable
    test_size: test size should be given in percentages like 0.25(25%) or 0.3(30%)
    """
    X = data.drop(target_column, axis=1).values
    y = data[target_column].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=101)
    m = RandomForestRegressor(n_jobs=-1, oob_score=True)
    m.fit(X_train, y_train)
    y_pred = m.predict(X_test)
    mae = metrics.mean_absolute_error(y_test, y_pred)
    mse = metrics.mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    mape = metrics.mean_absolute_percentage_error(y_test, y_pred)
    VarScore = metrics.explained_variance_score(y_test, y_pred)
    r_square = metrics.r2_score(y_test, y_pred)

    scores = {"mae": mae, "mse": mse, "rmse": rmse, "mape": mape, "VarScore": VarScore, "r_square": r_square}

    return scores, y_test, y_pred
