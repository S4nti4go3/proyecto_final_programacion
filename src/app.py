import os
from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
from datetime import datetime
from dotenv import load_dotenv

# ============================
# Cargar archivo .env
# ============================
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

# ============================
# Obtener cadena de conexión
# ============================
mongo_uri = os.environ.get('MONGO_URI')

if not mongo_uri:
    print("❌ Error: La variable de entorno MONGO_URI no está configurada en .env")

print("Intentando conectar a MongoDB Atlas...")

app.config["MONGO_URI"] = mongo_uri

# ============================
# Conectarse a MongoDB
# ============================
try:
    mongo = PyMongo(app)

    # usar DB: iot_db
    db = mongo.db

    # COLLECCIÓN REAL EN ATLAS:
    sensor_collection = db.sensor_data

    print("✅ Conexión a MongoDB Atlas establecida (DB: iot_db, Collection: sensor_data)")
    
    sensor_collection.find_one()  # test
    print("✅ Lectura de prueba exitosa.")

except Exception as e:
    print(f"❌ Error al conectar o interactuar con MongoDB Atlas: {e}")
    mongo = None
    sensor_collection = None


# ============================
# Rutas
# ============================

@app.route('/')
def home():
    return 'Servidor Flask funcionando correctamente 👍'


@app.route('/agregar_dato_prueba')
def agregar_dato_prueba():
    """
    Inserta un dato ficticio en sensor_data
    """
    if sensor_collection is None:
        return jsonify({"error": "No hay conexión a base de datos"}), 500

    try:
        dato = {
            "sensor": "temperatura_prueba",
            "valor": 25.7,
            "unidad": "C",
            "timestamp": datetime.utcnow()
        }

        result = sensor_collection.insert_one(dato)

        return jsonify({
            "mensaje": "Dato de prueba insertado correctamente",
            "id": str(result.inserted_id)
        }), 200

    except Exception as e:
        return jsonify({"error": f"No se pudo insertar: {e}"}), 500


@app.route('/receive_sensor_data', methods=['POST'])
def receive_sensor_data():
    """
    Recibe datos reales enviados por el ESP32 / Wokwi
    """
    if sensor_collection is None:
        return jsonify({"error": "No hay conexión con MongoDB"}), 503

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Payload JSON vacío"}), 400

        sensor_type = data.get('sensor_type')
        value = data.get('value')
        unit = data.get('unit', 'N/A')

        if sensor_type is None or value is None:
            return jsonify({"error": "Faltan campos obligatorios: sensor_type o value"}), 400

        doc = {
            "sensor": sensor_type,
            "valor": value,
            "unidad": unit,
            "timestamp": datetime.utcnow()
        }

        result = sensor_collection.insert_one(doc)

        return jsonify({
            "status": "success",
            "message": "Dato recibido y guardado 👍",
            "id_mongo": str(result.inserted_id),
            "data_received": doc
        }), 201

    except Exception as e:
        print(f"Error en receive_sensor_data: {e}")
        return jsonify({"status": "error", "message": f"Error interno: {e}"}), 500


