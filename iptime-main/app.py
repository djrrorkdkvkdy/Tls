from flask import Flask, render_template, request, jsonify
import cv2
import mediapipe as mp
import numpy as np
import base64
from tensorflow.keras.models import load_model

app = Flask(__name__)

model = load_model("model/hand_model.h5")

with open("labels.txt", encoding="utf-8") as f:
    labels = [line.strip() for line in f.readlines() if line.strip()]

LABEL_ALIASES = {
    "pip install tensorflow==2.15.0 protobuf==3.20.3": "손 펼치기",
}


def display_label(raw_label):
    if raw_label == "No Hand":
        return raw_label
    return LABEL_ALIASES.get(raw_label, raw_label)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.7,
)


def predict_from_frame(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    prediction = "No Hand"
    landmarks = None

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        landmarks = [[lm.x, lm.y] for lm in hand_landmarks.landmark]

        data = []
        for lm in hand_landmarks.landmark:
            data.append(lm.x)
            data.append(lm.y)

        data = np.array(data).reshape(1, -1)
        pred = model.predict(data, verbose=0)
        prediction = labels[np.argmax(pred)]

    return prediction, landmarks


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True)
    if not payload or "image" not in payload:
        return jsonify({"prediction": "No Hand", "landmarks": None})

    image_data = payload["image"]
    if "," in image_data:
        image_data = image_data.split(",", 1)[1]

    try:
        img_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except (ValueError, TypeError):
        return jsonify({"prediction": "No Hand", "landmarks": None})

    if frame is None:
        return jsonify({"prediction": "No Hand", "landmarks": None})

    prediction, landmarks = predict_from_frame(frame)
    return jsonify({
        "prediction": display_label(prediction),
        "landmarks": landmarks,
    })


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
