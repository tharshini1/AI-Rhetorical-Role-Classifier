from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import torch

app = Flask(__name__)

# ----------------------------------------------------
# Load Model (Loads once when server starts)
# ----------------------------------------------------

MODEL_NAME = "YOUR_HUGGINGFACE_MODEL"

try:
    classifier = pipeline(
        "text-classification",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME,
        device=0 if torch.cuda.is_available() else -1
    )
    model_loaded = True
except Exception as e:
    print("Model Loading Error:", e)
    classifier = None
    model_loaded = False


# ----------------------------------------------------
# Home Page
# ----------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------------------------------
# Prediction API
# ----------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    if not model_loaded:
        return jsonify({
            "success": False,
            "message": "Model failed to load."
        })

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No JSON received."
        })

    text = data.get("text", "").strip()

    if text == "":
        return jsonify({
            "success": False,
            "message": "Please enter some text."
        })

    try:

        prediction = classifier(text)

        label = prediction[0]["label"]
        confidence = round(prediction[0]["score"] * 100, 2)

        return jsonify({
            "success": True,
            "prediction": label,
            "confidence": confidence
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })


# ----------------------------------------------------
# Health Check
# ----------------------------------------------------

@app.route("/health")
def health():
    return jsonify({
        "status": "Running"
    })


# ----------------------------------------------------
# Run Application
# ----------------------------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
