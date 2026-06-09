from flask import Flask, request, render_template
import joblib
import numpy as np
from PIL import Image

app = Flask(__name__)

model = joblib.load("savedmodel.pth")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]

    img = Image.open(file).convert("L")
    img = img.resize((64, 64))

    img = np.array(img).flatten()
    img = img.reshape(1, -1)

    prediction = model.predict(img)

    return f"Predicted Class: {prediction[0]}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)