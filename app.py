import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify

# Init Flask
app = Flask(__name__)

# Init Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    return jsonify({"message": "Flask + Firebase connected"})

# Example: IoT device sends data
@app.route('/add-data', methods=['POST'])
def add_data():
    data = request.json
    doc_ref = db.collection("iot_data").add(data)
    return jsonify({"status": "success", "id": str(doc_ref[1].id)})

# Example: Get all IoT data
@app.route('/get-data', methods=['GET'])
def get_data():
    docs = db.collection("iot_data").stream()
    data_list = [{doc.id: doc.to_dict()} for doc in docs]
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(debug=True)