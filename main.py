import ujson
import urequests
import time
import network
import random

# ============================
# CONFIGURACIÓN
# ============================

WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""

SERVER_URL = "https://proyecto-final-programacion-i5d4.onrender.com/receive"

# ============================
# CONEXIÓN WIFI
# ============================

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    print("Conectando al WiFi...")
    wlan.connect(WIFI_SSID, WIFI_PASS)

    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        print(".", end="")
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("\n✅ WiFi conectado")
        print("IP:", wlan.ifconfig()[0])
        return wlan
    else:
        print("\n❌ Error de conexión WiFi")
        return None

# ============================
# SIMULACIÓN DE SENSORES
# ============================

def read_simulated_data(sensor_type):
    if sensor_type == "Temperature":
        value = random.uniform(20.0, 36.0)
        return round(value, 1), "C"
    elif sensor_type == "Humidity":
        value = random.uniform(40.0, 71.0)
        return round(value, 1), "%"
    return None, None

# ============================
# ENVÍO DE DATOS
# ============================

def send_data(sensor_type):
    value, unit = read_simulated_data(sensor_type)
    if value is None:
        print("❌ Tipo de sensor no válido")
        return
    
    payload = {
        "sensor_type": sensor_type,
        "value": value,
        "unit": unit
    }

    print("\n📤 Enviando:", payload)

    try:
        response = urequests.post(
            SERVER_URL,
            data=ujson.dumps(payload),
            headers={"Content-Type": "application/json"}
        )

        print("➡️ HTTP:", response.status_code)
        print("➡️ Respuesta:", response.text)
        response.close()

    except Exception as e:
        print("❌ Error al enviar:", e)

# ============================
# LOOP PRINCIPAL
# ============================

def main():
    if connect_wifi():
        while True:
            send_data("Temperature")
            time.sleep(2)

            send_data("Humidity")
            print("⌛ Esperando 15s...\n")
            time.sleep(15)


main()
