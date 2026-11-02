# # train_model.py
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import classification_report, accuracy_score
# import joblib

# # Load and clean dataset
# df = pd.read_csv("shopping_trends.csv")
# df = df[['Age', 'Gender', 'Category', 'Size', 'Season', 'Item Purchased']]
# df.dropna(inplace=True)

# # Label encoding
# le_dict = {}
# for col in ['Gender', 'Category', 'Size', 'Season', 'Item Purchased']:
#     le = LabelEncoder()
#     df[col] = le.fit_transform(df[col])
#     le_dict[col] = le

# # Features and target
# X = df[['Age', 'Gender', 'Category', 'Size', 'Season']]
# y = df['Item Purchased']

# # Split and train
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Evaluate
# y_pred = model.predict(X_test)
# print("Accuracy:", accuracy_score(y_test, y_pred))
# # print("Classification Report:\n", classification_report(y_test, y_pred))

# # Save model and encoders
# # joblib.dump(model, "item_predictor_model.pkl")
# # joblib.dump(le_dict, "label_encoders.pkl")

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# --- Step 1: Data Loading and Preparation ---
# Load the dataset from the CSV file.
print("Loading data...")
try:
    df = pd.read_csv(Path(__file__).resolve().parent / 'shopping_trends.csv')
except FileNotFoundError:
    print("Error: The file 'shopping_trends.csv' was not found next to this script.")
    exit()

# Define the features (X) and the target variable (y).
# The inputs are 'Age', 'Gender', 'Category', 'Size', and 'Season'.
# The model will predict 'Item Purchased'.
features = ['Age', 'Gender', 'Category', 'Size', 'Season']
target = 'Item Purchased'

X = df[features]
y = df[target]

# --- Step 2: Data Cleaning and Preprocessing ---
# Identify categorical and numerical features for preprocessing.
categorical_features = ['Gender', 'Category', 'Size', 'Season']
numerical_features = ['Age']

# Create a preprocessing pipeline for the features.
# OneHotEncoder is used for categorical features to convert them into a numerical format
# that the model can understand. We use handle_unknown='ignore' to gracefully handle
# any new categories that might appear in the test set, although this is unlikely here.
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', 'passthrough', numerical_features)
    ])

# Split the data into training and testing sets.
# This is crucial for evaluating the model's performance on unseen data.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Step 3: Model Training ---
# Create a machine learning pipeline that combines the preprocessor and the model.
# This ensures that the same preprocessing steps are applied consistently to both
# the training and testing data.
# RandomForestClassifier is chosen as a robust model for this type of multi-class classification problem.
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

print("Training the model...")
model.fit(X_train, y_train)
print("Model training complete.")

# --- Step 4: Prediction and Accuracy Evaluation ---
# Make predictions on the test set.
print("Making predictions on the test data...")
y_pred = model.predict(X_test)

# Calculate the accuracy of the model.
# Accuracy is the proportion of correctly predicted instances.
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# --- Example of a new prediction ---
# You can use the trained model to predict 'Item Purchased' for a new, unseen data point.
# Let's create a hypothetical customer.
new_customer = pd.DataFrame([{
    'Age': 55,
    'Gender': 'Male',
    'Category': 'Clothing',
    'Size': 'M',
    'Season': 'Summer'
}])

# Make a prediction for the new customer.
predicted_item = model.predict(new_customer)
print(f"\nExample Prediction:")
print(f"Input: {new_customer.iloc[0].to_dict()}")
print(f"Predicted Item Purchased: {predicted_item[0]}")