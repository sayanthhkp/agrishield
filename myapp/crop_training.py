# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder, StandardScaler
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score, classification_report
# import joblib
#
# # Load the dataset
# df = pd.read_csv(r'C:\Users\alen kurian\PycharmProjects\agrishiled\myapp\static\data_core.csv')  # Replace with your actual filename
#
# # Take first 500 rows
# df = df.head(5000)
#
# print(f"Dataset shape: {df.shape}")
# print(f"Columns: {df.columns.tolist()}")
#
# # Data preprocessing
# # Separate features and target
# X = df.drop('Crop Type', axis=1)
# y = df['Crop Type']
#
# # Identify categorical and numerical columns
# categorical_cols = ['Soil Type']
# numerical_cols = [col for col in X.columns if col not in categorical_cols]
#
# # Encode categorical variables
# label_encoders = {}
# for col in categorical_cols:
#     le = LabelEncoder()
#     X[col] = le.fit_transform(X[col])
#     label_encoders[col] = le
#     print(f"Encoded {col}: {le.classes_}")
#
# # Encode target variable
# label_encoder_y = LabelEncoder()
# y_encoded = label_encoder_y.fit_transform(y)
# print(f"Encoded target classes: {label_encoder_y.classes_}")
#
# # Split the data
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
# )
#
# print(f"\nTraining set size: {X_train.shape}")
# print(f"Testing set size: {X_test.shape}")
#
# # Standardize numerical features (optional but often helpful)
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)
#
# # Train Random Forest model
# print("\nTraining Random Forest model...")
# rf_model = RandomForestClassifier(
#     n_estimators=100,
#     max_depth=10,
#     random_state=42,
#     n_jobs=-1  # Use all available cores
# )
#
# rf_model.fit(X_train_scaled, y_train)
#
# # Make predictions
# y_pred = rf_model.predict(X_test_scaled)
# y_pred_proba = rf_model.predict_proba(X_test_scaled)
#
# # Evaluate the model
# accuracy = accuracy_score(y_test, y_pred)
# print(f"\nModel Accuracy: {accuracy:.4f}")
# print("\nClassification Report:")
# print(classification_report(y_test, y_pred, target_names=label_encoder_y.classes_))
#
# # Feature importance
# feature_importance = pd.DataFrame({
#     'feature': X.columns,
#     'importance': rf_model.feature_importances_
# }).sort_values('importance', ascending=False)
#
# print("\nFeature Importance:")
# print(feature_importance)
#
# # Save the model and preprocessing objects
# print("\nSaving model and preprocessing objects...")
#
# # Create a dictionary to store all components
# model_package = {
#     'model': rf_model,
#     'scaler': scaler,
#     'label_encoders': label_encoders,
#     'label_encoder_y': label_encoder_y,
#     'feature_names': X.columns.tolist(),
#     'categorical_cols': categorical_cols,
#     'numerical_cols': numerical_cols
# }
#
# # Save using joblib
# joblib.dump(model_package, r'C:\Users\alen kurian\PycharmProjects\agrishiled\myapp\static\random_forest_crop_model.pkl')
# print("Model saved as 'random_forest_crop_model.pkl'")
#
# # Also save individual components if needed
# joblib.dump(rf_model, r'C:\Users\alen kurian\PycharmProjects\agrishiled\myapp\static\rf_model.joblib')
# joblib.dump(scaler, r'C:\Users\alen kurian\PycharmProjects\agrishiled\myapp\static\scaler.joblib')
# joblib.dump(label_encoder_y, r'C:\Users\alen kurian\PycharmProjects\agrishiled\myapp\static\label_encoder_y.joblib')
#
# print("\nIndividual components also saved as separate files.")
#
# # Example of loading and using the model
# print("\n" + "="*50)
# print("Example of loading and using the saved model:")
# print("="*50)
#
# # Load the model
# loaded_package = joblib.load(r'C:\Users\alen kurian\PycharmProjects\agrishiled\myapp\static\random_forest_crop_model.pkl')
# loaded_model = loaded_package['model']
# loaded_scaler = loaded_package['scaler']
# loaded_label_encoders = loaded_package['label_encoders']
# loaded_label_encoder_y = loaded_package['label_encoder_y']
#
# # Create a sample input for prediction
# sample_data = pd.DataFrame([{
#     'Temparature': 28,
#     'Humidity': 54,
#     'Moisture': 38,
#     'Soil Type': 'Clayey',
#     'Nitrogen': 37,
#     'Potassium': 0,
#     'Phosphorous': 0
# }])
#
# # Preprocess the sample data
# for col in loaded_package['categorical_cols']:
#     if col in loaded_label_encoders:
#         sample_data[col] = loaded_label_encoders[col].transform(sample_data[col])
#
# # Scale the features
# sample_scaled = loaded_scaler.transform(sample_data)
#
# # Make prediction
# prediction_encoded = loaded_model.predict(sample_scaled)
# prediction = loaded_label_encoder_y.inverse_transform(prediction_encoded)
#
# print(f"\nSample prediction:")
# print(f"Input: {sample_data.iloc[0].to_dict()}")
# print(f"Predicted Crop Type: {prediction[0]}")
#
#
# soil_mapping = {"Black" : 0, "Clayey" : 1, "Loamy" : 2, "Red" : 3, "Sandy" : 4}
# crop_mapping = {"Barley" : 0, "Cotton" : 1, "Ground Nuts" : 2, "Maize" : 3, "Millets" : 4, "Oil Seeds":5, "Paddy":6, "Pulses":7, "Sugarcane":8,
#                     "Tobacco":9, "Wheat":10}
#
#
#
# data=[24.4,59.68,29.94,"Clayey",9,19,19]
# data[3]=soil_mapping[data[3]]
# print(data)
#
#
# sample_scaled2 = loaded_scaler.transform([data])
#
# # Make prediction
# prediction_encoded2 = loaded_model.predict(sample_scaled2)
# prediction2 = loaded_label_encoder_y.inverse_transform(prediction_encoded2)
# print("Prediction 2 : ", prediction2)
#
import joblib

soil_mapping = {"Black" : 0, "Clayey" : 1, "Loamy" : 2, "Red" : 3, "Sandy" : 4}
crop_mapping = {"Barley" : 0, "Cotton" : 1, "Ground Nuts" : 2, "Maize" : 3, "Millets" : 4, "Oil Seeds":5, "Paddy":6, "Pulses":7, "Sugarcane":8,
                    "Tobacco":9, "Wheat":10}
data=[33.07,62.75,57.16,"Clayey",7,11,27]
data[3]=soil_mapping[data[3]]
print(data)

model=joblib.load(r"C:\Users\alen kurian\PycharmProjects\agrishiled\myapp\static\rf_model.joblib")
pred=model.predict([data])
print("Pred ", pred)