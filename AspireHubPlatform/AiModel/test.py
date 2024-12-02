from flask import Flask, request, jsonify
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Initialize Flask app
app = Flask(__name__)

# Load the trained model and label encoders
rf_model = joblib.load('random_forest_model.pkl')
label_mappings = joblib.load('label_mappings.pkl')

# Route to predict future career
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from POST request
        data = request.json  # Expecting input in JSON format
        
        # Convert the input data to a DataFrame
        data_df = pd.DataFrame(data, index=[0])
        
        # Encode the categorical features using saved label encoders
        for col in data_df.columns:
            if data_df[col].dtype == 'object':
                le = LabelEncoder()
                le.classes_ = label_mappings[col].keys()  # Load saved classes
                data_df[col] = le.transform(data_df[col])
        
        # Make prediction using the loaded model
        prediction = rf_model.predict(data_df)
        
        # Decode the prediction to the original label (Future Career)
        predicted_label = label_mappings["Future Career"]
        decoded_prediction = {v: k for k, v in predicted_label.items()}[prediction[0]]

        # Return the predicted future career
        return jsonify({'predicted_future_career': decoded_prediction})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)