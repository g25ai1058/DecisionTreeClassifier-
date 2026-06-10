from flask import Flask, render_template, request
from sklearn.datasets import fetch_olivetti_faces
import joblib

app = Flask(__name__)

model = joblib.load("savedmodel.pth")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    image_id = int(request.form["image_id"])

    faces = fetch_olivetti_faces()

    sample = faces.data[image_id].reshape(1, -1)

    prediction = model.predict(sample)[0]

    return render_template(
        "index.html",
        prediction=f"Predicted Person ID: {prediction}"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
