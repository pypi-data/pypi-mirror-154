import os
import sys
import pandas as pd
import mlflow
from sklearn.model_selection import train_test_split

fpath = sys.argv[1]

data_path = os.getcwd() + "\\house_data.csv"
Data = pd.read_csv(data_path)

remote_server_uri = "http://127.0.0.1:5000"  # set to your server URI
mlflow.set_tracking_uri(remote_server_uri)  # or set the MLFLOW_TRACKING_URI in the env

with mlflow.start_run(run_name="Data Prep") as parent_run:
    mlflow.log_param("parent", "yes")
    Data = Data.drop("date", axis=1)
    Data = Data.drop("id", axis=1)
    Data = Data.drop("zipcode", axis=1)

    X = Data.drop("price", axis=1).values
    y = Data["price"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)
    try:
        os.makedirs(fpath)
    except FileExistsError:
        # directory already exists
        pass

    pd.DataFrame(X_train).to_csv(os.path.join(fpath, "X_train.csv"), index=False)
    pd.DataFrame(X_test).to_csv(os.path.join(fpath, "X_test.csv"), index=False)
    pd.DataFrame(y_train).to_csv(os.path.join(fpath, "y_train.csv"), index=False)
    pd.DataFrame(y_test).to_csv(os.path.join(fpath, "y_test.csv"), index=False)

    print("files exported")
