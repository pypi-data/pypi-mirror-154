from sklearn.ensemble import RandomForestRegressor
import mlflow
import pickle
import pandas as pd
import os
import sys

fpath = sys.argv[1]
# fpath = "C:\\Users\\saikumar.godha\\Downloads\\basic_regg_lib\\output_folder"

X_train = pd.read_csv(os.path.join(fpath, "X_train.csv"))
X_test = pd.read_csv(os.path.join(fpath, "X_test.csv"))
y_train = pd.read_csv(os.path.join(fpath, "y_train.csv"))
y_test = pd.read_csv(os.path.join(fpath, "y_test.csv"))

with mlflow.start_run(run_name="Model") as parent_run:
    mlflow.log_param("parent", "yes")
    m = RandomForestRegressor(n_jobs=-1, oob_score=True)
    m.fit(X_train, y_train)

    # save the model to disk
    filename = os.path.join(fpath, "model.pickle")
    pickle.dump(m, open(filename, "wb"))

    print("model saved")
