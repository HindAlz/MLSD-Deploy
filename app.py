import pandas as pd
from flask import Flask, request, jsonify
from autogluon.tabular import TabularPredictor

from feature_schema import validate_manual_features

app = Flask(__name__)

PREDICTOR = TabularPredictor.load(require_py_version_match=False, path="autogluon_model")
THRESHOLD = 0.11

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

def predict_from_features(features: dict):
    validated = validate_manual_features(features)
    df_input = pd.DataFrame([validated])

    for col in ["profile pic", "name==username", "external URL", "private"]:
        if col in df_input.columns:
            df_input[col] = df_input[col].astype(str)

    prob_df = PREDICTOR.predict_proba(df_input)

    if 1 in prob_df.columns:
        prob_fake = float(prob_df[1].iloc[0])
    elif "1" in prob_df.columns:
        prob_fake = float(prob_df["1"].iloc[0])
    else:
        prob_fake = float(prob_df.iloc[0, -1])

    pred = int(prob_fake >= THRESHOLD)

    return {
        "features": validated,
        "prediction": "fake" if pred == 1 else "not fake",
        "probability_fake": prob_fake,
        "threshold": THRESHOLD,
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

        return jsonify({"error": "Invalid mode. Use 'manual'"}), 400

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)