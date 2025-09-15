import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from datetime import datetime, timezone

# Flask init
app = Flask(__name__)

# Firebase init
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    return jsonify({"message": "Flask + Firebase IoT backend running"})

# IoT data endpoint
@app.route('/add-data', methods=['GET', 'POST'])
def add_data():
    try:
        if request.method == 'GET':
            return (
                """
                <html>
                <head><title>Add IoT Data</title></head>
                <body>
                  <h3>POST /add-data</h3>
                  <p>This form sends JSON to the API.</p>
                  <form id="f">
                    <textarea id="json" rows="10" cols="60">{"sensor_type":"temperature","value":25.5,"location":"room1"}</textarea><br/>
                    <button type="button" onclick="send()">Send</button>
                  </form>
                  <pre id="out"></pre>
                  <script>
                    async function send(){
                      const body = document.getElementById('json').value;
                      const res = await fetch('/add-data', {method:'POST', headers:{'Content-Type':'application/json'}, body});
                      const txt = await res.text();
                      document.getElementById('out').textContent = res.status + ' ' + res.statusText + '\n' + txt;
                    }
                  </script>
                </body>
                </html>
                """,
                200,
                {"Content-Type": "text/html"}
            )

        # Basic diagnostics to help debug 400s during development
        # Note: Avoid dumping sensitive info in production logs
        print("/add-data headers:", dict(request.headers))

        if not request.is_json:
            return jsonify({
                "status": "error",
                "message": "Content-Type must be application/json"
            }), 400

        # Log raw body to help diagnose malformed JSON from devices
        # Use cache=True so subsequent get_json can still read the body
        raw_body = request.get_data(cache=True)
        print("/add-data raw length:", len(raw_body))
        try:
            print("/add-data raw preview:", raw_body[:200])
            print("/add-data raw hex:", raw_body[:64].hex())
        except Exception:
            pass

        # Parse JSON with explicit error report
        try:
            data = request.get_json(force=False, silent=False)
        except Exception as parse_err:
            return jsonify({
                "status": "error",
                "message": f"Invalid JSON body: {str(parse_err)}",
                "raw_length": len(raw_body),
                "raw_preview": raw_body[:200].decode(errors='replace'),
                "raw_hex": raw_body[:64].hex()
            }), 400

        if not data:
            return jsonify({
                "status": "error",
                "message": "Empty JSON body"
            }), 400

        # Add server timestamp if missing
        if "timestamp" not in data:
            data["timestamp"] = datetime.now(timezone.utc).isoformat()

        doc_ref = db.collection("iot_data").add(data)
        return jsonify({"status": "success", "id": doc_ref[1].id}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/get-data', methods=['GET'])
def get_data():
    docs = db.collection("iot_data").stream()
    data_list = [{doc.id: doc.to_dict()} for doc in docs]
    return jsonify(data_list)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        docs = db.collection("iot_data").order_by("timestamp").stream()
    except Exception:
        # Fallback if timestamp field may not exist yet
        docs = db.collection("iot_data").stream()

    rows_html = []
    for doc in docs:
        data = doc.to_dict() or {}
        timestamp = data.get("timestamp", "-")
        device_id = data.get("device_id", "-")
        sensor_type = data.get("sensor_type", data.get("type", "-"))
        value = data.get("value", data.get("reading", data.get("sensor1", data)))
        rows_html.append(
            f"<tr><td>{doc.id}</td><td>{timestamp}</td><td>{device_id}</td><td>{sensor_type}</td><td>{value}</td><td><pre style=\"margin:0\">{data}</pre></td></tr>"
        )

    html = f"""
    <html>
    <head>
      <title>IoT Dashboard</title>
      <meta http-equiv="refresh" content="5">
      <style>
        body {{ font-family: Arial, sans-serif; padding: 16px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
        th {{ background: #f3f3f3; }}
      </style>
    </head>
    <body>
      <h2>IoT Readings</h2>
      <p>Auto-refreshes every 5s</p>
      <table>
        <thead>
          <tr>
            <th>Document ID</th>
            <th>Timestamp</th>
            <th>Device ID</th>
            <th>Sensor Type</th>
            <th>Value</th>
            <th>Raw</th>
          </tr>
        </thead>
        <tbody>
          {''.join(rows_html) or '<tr><td colspan=6>No data</td></tr>'}
        </tbody>
      </table>
    </body>
    </html>
    """
    return html, 200, {"Content-Type": "text/html"}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)  # allow ESP32 to reach Flask
