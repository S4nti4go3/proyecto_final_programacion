from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Conexión a MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["iot_db"]
sensor_collection = db["sensor_data"]

# Crear la app Flask
app = Flask(__name__)

@app.route("/", methods=["POST"])
def receive_data():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON recibido"}), 400

    # Guardar en MongoDB
    result = sensor_collection.insert_one(data)
    return jsonify({"status": "success", "id": str(result.inserted_id)}), 201

# Ejecutar app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
