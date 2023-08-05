from __init__ import rfregression
import os
import pandas as pd

path = os.path.dirname(os.path.abspath(__file__))
path = path + "\house_data.csv"
print(path)
data = pd.read_csv(path)

data = data.drop("date", axis=1)
data = data.drop("id", axis=1)
data = data.drop("zipcode", axis=1)

scores, y_test, y_pred = rfregression(data, "price", 0.3)

print(scores)
