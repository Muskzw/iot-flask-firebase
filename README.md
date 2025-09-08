# IoT Flask Firebase Project

A simple Flask web application that integrates with Firebase Firestore to handle IoT device data. This project provides REST API endpoints for IoT devices to send data and retrieve stored information.

## Features

- 🔥 **Firebase Integration**: Uses Firebase Admin SDK for Firestore database operations
- 🌐 **REST API**: Simple endpoints for IoT data management
- 📊 **Data Storage**: Store and retrieve IoT sensor data
- 🚀 **Flask Framework**: Lightweight and easy to deploy

## API Endpoints

### GET `/`
- **Description**: Health check endpoint
- **Response**: `{"message": "Flask + Firebase connected"}`

### POST `/add-data`
- **Description**: Add new IoT data to Firestore
- **Request Body**: JSON object with IoT sensor data
- **Response**: 
  ```json
  {
    "status": "success",
    "id": "document_id"
  }
  ```

### GET `/get-data`
- **Description**: Retrieve all IoT data from Firestore
- **Response**: Array of IoT data documents
  ```json
  [
    {
      "document_id": {
        "sensor_type": "temperature",
        "value": 25.5,
        "timestamp": "2024-01-01T12:00:00Z"
      }
    }
  ]
  ```

## Prerequisites

- Python 3.7+
- Firebase project with Firestore enabled
- Firebase service account key

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd iot-flask-firebase
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install flask firebase-admin
   ```

5. **Set up Firebase**
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Enable Firestore Database
   - Generate a service account key:
     - Go to Project Settings → Service Accounts
     - Click "Generate new private key"
     - Download the JSON file and rename it to `firebase-key.json`
     - Place it in the project root directory

## Configuration

Make sure your `firebase-key.json` file is in the project root directory. This file contains your Firebase service account credentials.

**⚠️ Security Note**: Never commit your `firebase-key.json` file to version control. Add it to your `.gitignore` file.

## Usage

1. **Start the Flask application**
   ```bash
   python app.py
   ```

2. **The server will start on** `http://localhost:5000`

3. **Test the endpoints**

   **Health Check:**
   ```bash
   curl http://localhost:5000/
   ```

   **Add IoT Data:**
   ```bash
   curl -X POST http://localhost:5000/add-data \
     -H "Content-Type: application/json" \
     -d '{"sensor_type": "temperature", "value": 25.5, "location": "room1"}'
   ```

   **Get All Data:**
   ```bash
   curl http://localhost:5000/get-data
   ```

## Project Structure

```
iot-flask-firebase/
├── app.py                 # Main Flask application
├── firebase-key.json      # Firebase service account key (not in git)
├── venv/                  # Virtual environment
└── README.md             # This file
```

## Example IoT Data Format

```json
{
  "sensor_type": "temperature",
  "value": 25.5,
  "unit": "celsius",
  "location": "living_room",
  "timestamp": "2024-01-01T12:00:00Z",
  "device_id": "sensor_001"
}
```

## Development

- The application runs in debug mode by default
- Flask will automatically reload when you make changes to the code
- Check the console for any error messages

## Deployment

For production deployment:

1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn
3. Set up proper environment variables for Firebase credentials
4. Configure your web server (nginx, Apache) as a reverse proxy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Note**: Remember to keep your Firebase service account key secure and never commit it to version control!
