from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(_name_)

# Load the trained ML model
model = joblib.load("plant_recommendation.pkl")

# Define API endpoint for prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        location = data['location']
        soil = data['soil']

        # Convert location and soil into numerical values if required
        # Example: Encoding location and soil types (You may modify this)
        location_mapping = {"Vijayawada": 1, "Delhi": 2, "Mumbai": 3}
        soil_mapping = {"Sandy": 1, "Clayey": 2, "Loamy": 3}

        location_value = location_mapping.get(location, 0)
        soil_value = soil_mapping.get(soil, 0)

        # Predict plant recommendations
        prediction = model.predict(np.array([[location_value, soil_value]]))

        return jsonify({'plants': prediction.tolist()})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if _name_ == '_main_':
    app.run(debug=True)