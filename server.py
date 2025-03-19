<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify
import joblib  # Use joblib instead of pickle
=======
from flask import Flask, render_template, request
import joblib
>>>>>>> 004ed6f8328a5d4901c04b6b57b86760c115cfb0
import pandas as pd

app = Flask(__name__)

<<<<<<< HEAD
# Load the trained model and encoders
try:
    model = joblib.load("./model/plant_recommendation_model.pkl")
    label_encoder = joblib.load("./model/label_encoder.pkl")
except Exception as e:
    print(f"❌ Error loading model or encoder: {e}")
    model, label_encoder = None, None

# Load datasets
try:
    soil_data = pd.read_csv("./model/newindia2.csv", encoding="utf-8")
    plant_data = pd.read_csv("./model/newplants5.csv", encoding="utf-8")
    
    # Standardize column names
    soil_data.columns = soil_data.columns.str.strip().str.lower()
    plant_data.columns = plant_data.columns.str.strip().str.lower()
    
    # Rename necessary columns to match expected names
    soil_data.rename(columns={"temperature (\u00b0c)": "temperature", "rainfall": "rainfall", "pH": "soil ph"}, inplace=True)
    plant_data.rename(columns={"temperature (\u00b0c)": "temperature", "rainfall": "rainfall", "pH": "soil ph"}, inplace=True)
    
    # Normalize location names
    soil_data["state"] = soil_data["state"].str.lower().str.strip()
    soil_data["district"] = soil_data["district"].str.lower().str.strip()
    plant_data["soil type"] = plant_data["soil type"].str.lower().str.strip()
except Exception as e:
    print(f"❌ Error loading datasets: {e}")
    soil_data, plant_data = None, None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None or label_encoder is None:
        return jsonify({"error": "Model or encoder could not be loaded!"})
    
    if soil_data is None or plant_data is None:
        return jsonify({"error": "Datasets could not be loaded!"})
    
    state = request.form.get("state", "").strip().lower()
    district = request.form.get("district", "").strip().lower()
    
    # Retrieve soil and climate data
    climate_data = soil_data[(soil_data["state"] == state) & (soil_data["district"] == district)]
    if climate_data.empty:
        return jsonify({"error": f"State '{state}' or District '{district}' not found in dataset!"})
    
    soil_type = climate_data["soil type"].values[0]
    temperature = climate_data["temperature"].values[0]
    rainfall = climate_data["rainfall"].values[0]
    ph = climate_data["soil ph"].values[0]

    # Prepare input for model
    input_data = pd.DataFrame([[ph, temperature, rainfall]], columns=["soil ph", "temperature", "rainfall"])

    # Predict suitable plants
    try:
        predictions = model.predict(input_data)  # Ensure model is a valid classifier
        predictions = label_encoder.inverse_transform(predictions)
        predictions = list(set(predictions))  # Remove duplicates
    except Exception as e:
        return jsonify({"error": f"Model prediction failed: {e}"})

    print("🔍 Predicted Plants:", predictions)  # Debugging Output

    # Get plant details (ensure unique plant names)
    recommended_plants = plant_data[plant_data["plant name"].isin(predictions)].drop_duplicates(subset=["plant name"])

    print("✅ Final Plant Recommendations:\n", recommended_plants)  # Debugging Output

    return render_template("result.html", state=state.capitalize(), district=district.capitalize(),
                           soil_type=soil_type, temperature=temperature, rainfall=rainfall, ph=ph,
                           plants=recommended_plants.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)

=======
# Load trained model
# model = joblib.load("model/plant_recommendation.pkl")

# Sample plant data
plant_data = {
    "loamy": ["Tomato", "Carrot", "Rose"],
    "sandy": ["Cactus", "Lavender", "Aloe Vera"],
    "clay": ["Willow Tree", "Sunflower", "Peony"]
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        location = request.form["location"]
        soil = request.form["soil"].lower()

        # Get plant recommendations
        recommended_plants = plant_data.get(soil, ["No recommendations found"])

        return render_template("result.html", location=location, soil=soil, plants=recommended_plants)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 004ed6f8328a5d4901c04b6b57b86760c115cfb0
