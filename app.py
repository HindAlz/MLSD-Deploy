import pandas as pd
from flask import Flask, request, jsonify
import joblib

from feature_schema import validate_manual_features

app = Flask(__name__)
MODEL = joblib.load("model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    mode = data.get("mode")

    if mode != "manual":
        return jsonify({"error": "Phase 1 only supports mode='manual'"}), 400

    try:
        features = validate_manual_features(data.get("features", {}))

        df_input = pd.DataFrame([features])

        # Convert categorical columns to string (must match training)
        for col in ["profile pic", "name==username", "external URL", "private"]:
            df_input[col] = df_input[col].astype(str)

        pred = int(MODEL.predict(df_input)[0])

        prob_fake = None
        if hasattr(MODEL, "predict_proba"):
            prob_fake = float(MODEL.predict_proba(df_input)[0][1])

        return jsonify({
            "prediction": "fake" if pred == 1 else "not fake",
            "probability_fake": prob_fake,
            "features": features
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500