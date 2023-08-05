import pickle
import mlflow
import numpy as np
import pandas as pd
from sklearn import metrics
import os
import sys

mpath = sys.argv[1]
fpath = sys.argv[2]
# mpath = "C:\\Users\\saikumar.godha\\Downloads\\basic_regg_lib\\output_folder\\model.pickle" #Pickle path
# fpath = "C:\\Users\\saikumar.godha\\Downloads\\basic_regg_lib\\output_folder" #csv files folder path

X_test = pd.read_csv(os.path.join(fpath, "X_test.csv"))
y_test = pd.read_csv(os.path.join(fpath, "y_test.csv"))

with mlflow.start_run(run_name="score") as parent_run:
    mlflow.log_param("parent", "yes")
    # load the model from disk
    loaded_model = pickle.load(open(mpath, "rb"))
    y_pred = loaded_model.predict(X_test)

    mae = metrics.mean_absolute_error(y_test, y_pred)
    mse = metrics.mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    mape = metrics.mean_absolute_percentage_error(y_test, y_pred)
    VarScore = metrics.explained_variance_score(y_test, y_pred)
    r_square = metrics.r2_score(y_test, y_pred)

    print(f"mae: {mae}, mse: {mse}, rmse: {rmse}, mape: {mape}, VarScore: {VarScore}, r_square: {r_square}")
