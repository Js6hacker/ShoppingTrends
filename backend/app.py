# # app.py
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import joblib
# import numpy as np

# app = Flask(__name__)
# CORS(app)


# # Load model and encoders
# model = joblib.load("item_predictor_model.pkl")
# le_dict = joblib.load("label_encoders.pkl")

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.json
#     try:
#         # Extract features
#         age = int(data['Age'])
#         gender = le_dict['Gender'].transform([data['Gender']])[0]
#         category = le_dict['Category'].transform([data['Category']])[0]
#         size = le_dict['Size'].transform([data['Size']])[0]
#         season = le_dict['Season'].transform([data['Season']])[0]
        
#         features = np.array([[age, gender, category, size, season]])
        
#         # Prediction
#         pred_encoded = model.predict(features)[0]
#         item = le_dict['Item Purchased'].inverse_transform([pred_encoded])[0]

#         return jsonify({'Predicted Item': item})
    
#     except Exception as e:
#         return jsonify({'error': str(e)})

# if __name__ == '__main__':
#     app.run(debug=True)


from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the entire trained pipeline, which includes the preprocessor and the classifier.
MODEL_PATH = Path(__file__).resolve().parent / "item_predictor_model.pkl"
try:
    model_pipeline = joblib.load(MODEL_PATH)
    print("Model pipeline loaded successfully.")
except FileNotFoundError:
    print(f"Error: model file not found at '{MODEL_PATH}'.")
    exit()

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to predict an 'Item Purchased' based on a JSON request.
    The JSON should contain 'Age', 'Gender', 'Category', 'Size', and 'Season'.
    """
    data = request.json
    try:
        # Create a pandas DataFrame from the incoming JSON data.
        # This is the correct format for the model pipeline.
        input_data = pd.DataFrame([data])
        
        # Use the loaded pipeline to make a prediction.
        # The pipeline handles all preprocessing internally.
        predicted_item = model_pipeline.predict(input_data)[0]
        
        # Return the prediction as a JSON response.
        return jsonify({'predicted_item': predicted_item})
    
    except KeyError as e:
        # Handle cases where the required keys are missing from the request.
        return jsonify({'error': f'Missing key in JSON payload: {str(e)}'}), 400
    except Exception as e:
        # Handle any other unexpected errors.
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the Flask application in debug mode.
    app.run(debug=True)