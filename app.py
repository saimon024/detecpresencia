import streamlit as st
import paho.mqtt.client as mqtt
import threading
import time

# ---------- CONFIG MQTT ----------
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "wowki/presencia"

# ---------- VARIABLE GLOBAL (thread-safe simple) ----------
presencia_detectada = False

# ---------- CALLBACKS MQTT (PAHO 1.6.1) ----------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    global presencia_detectada
    payload = msg.payload.decode()

    if payload == "1":
        presencia_detectada = True
    elif payload == "0":
        presencia_detectada = False

# ---------- HILO MQTT ----------
def mqtt_loop():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_forever()

# ---------- INICIAR MQTT UNA SOLA VEZ ----------
if "mqtt_started" not in st.session_state:
    threading.Thread(target=mqtt_loop, daemon=True).start()
    st.session_state.mqtt_started = True

# ---------- UI STREAMLIT ----------
st.title("Detector de Presencia (MQTT)")

if presencia_detectada:
    st.success("👀 Presencia detectada")
    st.audio("audio.mp3", autoplay=True)
else:
    st.info("Esperando presencia...")

st.caption("ESP32 (Wokwi) → MQTT → Streamlit")

# ---------- FORZAR REFRESH ----------
time.sleep(0.5)
st.experimental_rerun()

