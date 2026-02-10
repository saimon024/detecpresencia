import streamlit as st
import paho.mqtt.client as mqtt
import threading

# ---------- CONFIG MQTT ----------
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "wowki/presencia"

# ---------- ESTADOS ----------
if "presencia" not in st.session_state:
    st.session_state.presencia = False

if "mqtt_started" not in st.session_state:
    st.session_state.mqtt_started = False

# ---------- CALLBACKS MQTT ----------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    if payload == "1":
        st.session_state.presencia = True
    elif payload == "0":
        st.session_state.presencia = False

# ---------- HILO MQTT ----------
def mqtt_worker():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_forever()

# ---------- INICIAR MQTT ----------
if not st.session_state.mqtt_started:
    threading.Thread(target=mqtt_worker, daemon=True).start()
    st.session_state.mqtt_started = True

# ---------- UI ----------
st.title("Detector de Presencia (MQTT)")

if st.session_state.presencia:
    st.success("👀 Presencia detectada")

    if st.button("Reproducir audio"):
        st.audio("audio.mp3")
else:
    st.info("Esperando presencia...")

st.caption("ESP32 (Wokwi) → MQTT → Streamlit")

