
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def train():
    soil_mapping = {"Black" : 0, "Clayey" : 1, "Loamy" : 2, "Red" : 3, "Sandy" : 4}
    crop_mapping = {"Barley" : 0, "Cotton" : 1, "Ground Nuts" : 2, "Maize" : 3, "Millets" : 4, "Oil seeds":5, "Paddy":6, "Pulses":7, "Sugarcane":8,
                    "Tobacco":9, "Wheat":10}

    data = pd.read_csv(r"C:\Users\alen kurian\PycharmProjects\agrishiled\myapp\static\data_core.csv")
    print(data)

    features=data.values[1:8001 , :7]
    labels=data.values[1:8001 , 7]
    # Convert features to DataFrame
    features_df = pd.DataFrame(features, columns=data.columns[:-1])
    labels_df = pd.DataFrame(labels, columns=[data.columns[-1]])
    # Map soil type
    features_df["Soil Type"] = features_df["Soil Type"].map(soil_mapping)
    labels_df["Crop Type"] = labels_df["Crop Type"].map(crop_mapping)
    # Convert back to numpy array if needed
    features = features_df.values
    labels = labels_df.values
    cnt=0
    for i in range(len(labels)):
        try:
            print(cnt, " : ", features[i], " - ", labels[i])
        except Exception as e:
            print("Stopped at ", cnt)
        cnt += 1
    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)
    rf=RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(x_train, y_train)
    joblib.dump(rf, r"C:\Users\alen kurian\PycharmProjects\agrishiled\myapp\static\rf_model.joblib")
    y_pred=rf.predict(x_test)
    acc=accuracy_score(y_test, y_pred)
    print(acc)
    print("Accuracy : ", round(acc*100, 2))
# train()

import numpy as np
# Simple debug to find problematic rows
data = pd.read_csv(r"C:\Users\alen kurian\PycharmProjects\agrishiled\myapp\static\data_core.csv")

# Check each column for problematic values
for col in data.columns:
    if pd.api.types.is_numeric_dtype(data[col]):
        print(f"\n{col}:")
        print(f"  NaN: {data[col].isna().sum()}")
        print(f"  Inf: {(data[col] == np.inf).sum() + (data[col] == -np.inf).sum()}")
        print(f"  Min: {data[col].min()}")
        print(f"  Max: {data[col].max()}")


train()