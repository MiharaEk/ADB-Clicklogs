from flask import Flask, request, jsonify, send_from_directory
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

# Serve index.html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Serve CSS
@app.route('/index.css')
def css():
    return send_from_directory('.', 'index.css')

# Serve images from 2x folder
@app.route('/2x/<path:filename>')
def serve_2x(filename):
    return send_from_directory('2x', filename)

# Endpoint to save taps
@app.route('/saveTaps', methods=['POST'])
def save_taps():
    data = request.json

    # Convert timestamps (sent as ISO strings from frontend)
    try:
        start = datetime.fromisoformat(data['startTime'].replace("Z", ""))
        end = datetime.fromisoformat(data['endTime'].replace("Z", ""))
        duration = (end - start).total_seconds()
    except Exception:
        duration = data['endTime'] - data['startTime']  # fallback if numbers

    record = {
        "tapSequence": data['tapSequence'],
        "startTime": data['startTime'],
        "endTime": data['endTime'],
        "duration": duration,
        "interfaceType": data['interfaceType'],
        "sessionId": data['sessionId'],
        "devicePlatform": data['devicePlatform']
    }

    # Save to Firestore
    db.collection("tap_logs").add(record)

    return jsonify({"status": "success", "record": record})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
