import streamlit as st
import paho.mqtt.client as mqtt
import threading
import time

# ---------- CONFIGURACIÓN MQTT ----------
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "wowki/presencia"

# ---------- ESTADO GLOBAL ----------
if "presencia" not in st.session_state:
    st.session_state.presencia = False

if "mqtt_started" not in st.session_state:
    st.session_state.mqtt_started = False


# ---------- CALLBACK MQTT ----------
def on_message(client, userdata, msg):
    payload = msg.payload.decode()

    if payload == "1":
        st.session_state.presencia = True
    elif payload == "0":
        st.session_state.presencia = False


# ---------- HILO MQTT ----------
def mqtt_listener():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC)
    client.loop_forever()


# ---------- INICIAR MQTT UNA SOLA VEZ ----------
if not st.session_state.mqtt_started:
    thread = threading.Thread(target=mqtt_listener, daemon=True)
    thread.start()
    st.session_state.mqtt_started = True


# ---------- INTERFAZ STREAMLIT ----------
st.title("Detector de Presencia (MQTT)")

if st.session_state.presencia:
    st.success("👀 Presencia detectada")
    st.audio("audio.mp3", autoplay=True)
else:
    st.info("Esperando presencia...")

st.caption("ESP32 → MQTT → Streamlit")
