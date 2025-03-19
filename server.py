from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

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