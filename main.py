import ujson
import urequests
import time
import network
import random

# ============================
# CONFIGURACIÓN WOKWI + API
# ============================

WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""

# ⚠️ CAMBIAR ESTA URL CUANDO DESPLIEGUES EL BACKEND EN RENDER
SERVER_URL = "https://proyecto-final-programacion-i5d4.onrender.com/"


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Conectando al WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)

        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            print(".", end="")
            time.sleep(1)
            timeout -= 1

        if not wlan.isconnected():
            print("\n❌ No se pudo conectar al WiFi")
            return None

    print("\n✅ WiFi conectado:", wlan.ifconfig())
    return wlan


def simulate_sensor(sensor_type):
    if sensor_type == "Temperature":
        return round(random.uniform(20.0, 36.0), 1), "C"
    if sensor_type == "Humidity":
        return round(random.uniform(40.0, 70.0), 1), "%"

    return None, None


def send_data(sensor_type):
    value, unit = simulate_sensor(sensor_type)

    payload = {
        "sensor_type": sensor_type,
        "value": value,
        "unit": unit
    }

    print("\n📤 Enviando ->", payload)

    try:
        response = urequests.post(
            SERVER_URL,
            data=ujson.dumps(payload),
            headers={"Content-Type": "application/json"}
        )

        print("➡️ Código HTTP:", response.status_code)
        print("➡️ Respuesta:", response.text)
        response.close()

    except Exception as e:
        print("❌ Error enviando:", e)


def main():
    if connect_wifi():
        while True:
            send_data("Temperature")
            time.sleep(2)
            send_data("Humidity")

            print("⏳ Esperando 15s...\n")
            time.sleep(15)


main()
