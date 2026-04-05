import pandas as pd
from flask import Flask, request, jsonify
import joblib

from feature_schema import validate_manual_features
from profile_fetcher import fetch_x_profile_from_url
from feature_extractor import extract_features_from_x_profile

app = Flask(__name__)
MODEL = joblib.load("model.pkl")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


def predict_from_features(features: dict):
    validated = validate_manual_features(features)
    df_input = pd.DataFrame([validated])

    for col in ["profile pic", "name==username", "external URL", "private"]:
        df_input[col] = df_input[col].astype(str)

    pred = int(MODEL.predict(df_input)[0])

    prob_fake = None
    if hasattr(MODEL, "predict_proba"):
        prob_fake = float(MODEL.predict_proba(df_input)[0][1])

    return {
        "features": validated,
        "prediction": "fake" if pred == 1 else "not fake",
        "probability_fake": prob_fake,
    }


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    mode = data.get("mode")

    try:
        if mode == "manual":
            features = data.get("features", {})
            result = predict_from_features(features)
            return jsonify({"mode": "manual", **result}), 200

        if mode == "url":
            url = data.get("url")
            if not url:
                return jsonify({"error": "Missing 'url'"}), 400

            raw_profile = fetch_x_profile_from_url(url)
            features = extract_features_from_x_profile(raw_profile)
            result = predict_from_features(features)

            return jsonify({
                "mode": "url",
                "platform": "x",
                "url": url,
                **result
            }), 200

        return jsonify({"error": "Invalid mode. Use 'manual' or 'url'."}), 400

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)