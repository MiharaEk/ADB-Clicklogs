from flask import Flask, request, jsonify, send_from_directory
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

#enable cors
from flask_cors import CORS

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
    try:
        # data = request.json
        data = request.get_json(force=True) or {}


        start_raw = data.get('startTime')
        end_raw = data.get('endTime')
        duration = None

        if start_raw and end_raw:
        # Convert timestamps (sent as ISO strings from frontend)
            try:
                start = datetime.fromisoformat(str(start_raw).replace("Z", ""))
                end = datetime.fromisoformat(str(end_raw).replace("Z", ""))
                duration = (end - start).total_seconds()
            except Exception:
                try:
                    # Fallback if numeric timestamps
                    duration = float(end_raw) - float(start_raw)
                except Exception:
                    duration = None

                # duration = data.get('endTime') - data.get('startTime')  # fallback if numbers

        record = {
            "tapSequence": data.get('tapSequence'),
            "startTime": start_raw,
            "endTime": end_raw,
            "duration": duration,
            "interfaceType": data.get('interfaceType'),
            "sessionId": data.get('sessionId'),
            "devicePlatform": data.get('devicePlatform'),
            "source": "hosted-frontend"
        }

        # Save to Firestore
        db.collection("tap_logs").add(record)

        return jsonify({"status": "success", "record": record}, 200)
    
    except Exception as e:
        print("Error in /saveTaps:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
