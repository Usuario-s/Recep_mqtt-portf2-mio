
import streamlit as st
import paho.mqtt.client as mqtt
import json
import time
import uuid
import threading
import html
from datetime import datetime

# =========================================================
# CONFIGURACIÓN DE LA PÁGINA
# =========================================================

st.set_page_config(
    page_title="MQTT Sensor Reader",
    page_icon="⌘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ESTILOS: TERMINAL / IDE
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #0D1117;
    --panel: #161B22;
    --panel-light: #1C2128;
    --border: #30363D;
    --text: #E6EDF3;
    --muted: #8B949E;
    --green: #3FB950;
    --blue: #79C0FF;
    --orange: #D29922;
    --red: #F85149;
    --purple: #D2A8FF;
}

.stApp {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: var(--text) !important;
    font-family: 'Fira Code', monospace !important;
}

p, label, .stMarkdown {
    color: var(--text);
}

.editor-header {
    background: #161B22;
    border: 1px solid var(--border);
    border-radius: 10px 10px 0 0;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.editor-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
}

.editor-filename {
    color: #C9D1D9;
    font-family: 'Fira Code', monospace;
    font-size: 12px;
    margin-left: 10px;
}

.editor-content {
    background: #0D1117;
    border: 1px solid var(--border);
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 24px;
    overflow-wrap: anywhere;
}

.code-title {
    color: #E6EDF3;
    font-family: 'Fira Code', monospace;
    font-size: clamp(20px, 3vw, 30px);
    font-weight: 700;
    margin-bottom: 12px;
}

.code-comment {
    color: #8B949E;
    font-family: 'Fira Code', monospace;
    font-size: 13px;
    line-height: 1.9;
    overflow-wrap: anywhere;
}

.syntax-green { color: #7EE787; }
.syntax-blue { color: #79C0FF; }
.syntax-purple { color: #D2A8FF; }
.syntax-orange { color: #FFA657; }

section[data-testid="stSidebar"] {
    background: #0D1117;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-family: 'Fira Code', monospace !important;
    color: #79C0FF !important;
}

section[data-testid="stSidebar"] p {
    color: #C9D1D9 !important;
}

.stTextInput input,
.stNumberInput input {
    background: #0D1117 !important;
    color: #E6EDF3 !important;
    border: 1px solid #30363D !important;
    border-radius: 6px !important;
    font-family: 'Fira Code', monospace !important;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: #58A6FF !important;
    box-shadow: 0 0 0 1px #58A6FF !important;
}

.stTextInput label,
.stNumberInput label {
    color: #C9D1D9 !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 12px !important;
}

.stButton > button {
    background: #238636;
    color: #FFFFFF !important;
    border: 1px solid rgba(240,246,252,0.1);
    border-radius: 6px;
    min-height: 42px;
    font-family: 'Fira Code', monospace;
    font-weight: 600;
    transition: background 0.15s ease;
}

.stButton > button:hover {
    background: #2EA043;
    border-color: #3FB950;
    color: #FFFFFF !important;
}

.stButton > button:focus {
    box-shadow: 0 0 0 2px #58A6FF !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 8px;
    padding: 14px;
}

div[data-testid="stMetric"] {
    background: #0D1117;
    border: 1px solid #30363D;
    border-radius: 7px;
    padding: 15px;
    min-width: 0;
}

div[data-testid="stMetricLabel"] {
    color: #8B949E !important;
    font-family: 'Fira Code', monospace;
    font-size: 12px;
    overflow-wrap: anywhere;
}

div[data-testid="stMetricValue"] {
    color: #7EE787 !important;
    font-family: 'Fira Code', monospace;
    font-size: 23px;
    overflow-wrap: anywhere;
}

div[data-testid="stExpander"] {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 7px;
}

div[data-testid="stExpander"] summary {
    color: #C9D1D9 !important;
    font-family: 'Fira Code', monospace;
}

div[data-testid="stAlert"] {
    border-radius: 6px;
}

div[data-testid="stJson"],
.stCode {
    border: 1px solid #30363D;
    border-radius: 7px;
}

hr {
    border-color: #30363D !important;
}

.status-bar {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 6px;
    padding: 11px 15px;
    font-family: 'Fira Code', monospace;
    font-size: 12px;
    color: #8B949E;
    margin: 16px 0 22px 0;
    overflow-wrap: anywhere;
}

.status-green {
    color: #3FB950;
    font-weight: 600;
}

.status-yellow {
    color: #D29922;
    font-weight: 600;
}

.status-red {
    color: #F85149;
    font-weight: 600;
}

.footer {
    color: #6E7681;
    font-family: 'Fira Code', monospace;
    font-size: 11px;
    border-top: 1px solid #30363D;
    margin-top: 35px;
    padding-top: 17px;
    text-align: center;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

@media (max-width: 640px) {
    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .editor-content {
        padding: 15px;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# ESTADO DE LA APLICACIÓN
# =========================================================

if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = None

if "last_read_time" not in st.session_state:
    st.session_state.last_read_time = None


# =========================================================
# COMPATIBILIDAD CON PAHO-MQTT
# =========================================================

def create_mqtt_client(client_id):
    """
    Crea un cliente compatible con distintas versiones
    de paho-mqtt.
    """

    try:
        # API utilizada por paho-mqtt 2.x
        return mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION1,
            client_id=client_id,
            protocol=mqtt.MQTTv311
        )
    except (AttributeError, TypeError):
        # Compatibilidad con versiones anteriores
        return mqtt.Client(
            client_id=client_id,
            protocol=mqtt.MQTTv311
        )


# =========================================================
# FUNCIÓN MQTT
# =========================================================

def get_mqtt_message(broker, port, topic, client_id, timeout=8):
    """
    Se conecta al broker, se suscribe al tópico y espera
    un mensaje hasta alcanzar el tiempo límite.
    """

    message_event = threading.Event()
    result = {
        "received": False,
        "payload": None,
        "error": None
    }

    client = None

    def on_connect(client, userdata, flags, rc, *extra):
        # En MQTT 3.1.1, rc == 0 significa conexión exitosa.
        try:
            if hasattr(rc, "value"):
                connection_code = rc.value
            else:
                connection_code = int(rc)

            if connection_code != 0:
                result["error"] = (
                    f"El broker rechazó la conexión. Código: "
                    f"{connection_code}"
                )
                message_event.set()
                return

            client.subscribe(topic, qos=0)

        except Exception as exc:
            result["error"] = f"Error al suscribirse: {exc}"
            message_event.set()

    def on_subscribe(client, userdata, mid, granted_qos, *extra):
        # La suscripción se confirma desde el callback.
        pass

    def on_message(client, userdata, message):
        try:
            raw_payload = message.payload.decode("utf-8")
        except UnicodeDecodeError:
            raw_payload = message.payload.decode(
                "utf-8",
                errors="replace"
            )

        try:
            payload = json.loads(raw_payload)
        except (json.JSONDecodeError, TypeError):
            payload = raw_payload

        result["payload"] = payload
        result["received"] = True
        message_event.set()

    def on_disconnect(client, userdata, *args):
        # Evita marcar como error una desconexión normal
        # después de recibir el mensaje.
        if not result["received"] and not result["error"]:
            pass

    try:
        broker = broker.strip()
        topic = topic.strip()
        client_id = client_id.strip()

        if not broker:
            return {"error": "La dirección del broker está vacía."}

        if not topic:
            return {"error": "El tópico MQTT está vacío."}

        if not client_id:
            return {"error": "El ID del cliente está vacío."}

        port = int(port)

        if not 1 <= port <= 65535:
            return {"error": "El puerto debe estar entre 1 y 65535."}

        client = create_mqtt_client(client_id)

        client.on_connect = on_connect
        client.on_message = on_message
        client.on_subscribe = on_subscribe
        client.on_disconnect = on_disconnect

        client.connect(broker, port, keepalive=30)
        client.loop_start()

        # Espera la llegada del mensaje o un error de conexión.
        message_event.wait(timeout)

        if result["error"]:
            return {"error": result["error"]}

        if not result["received"]:
            return {
                "error": (
                    f"Tiempo de espera agotado ({timeout} segundos). "
                    "No llegó ningún mensaje al tópico indicado. "
                    "Verifica que otro dispositivo esté publicando "
                    "datos en ese mismo tópico."
                )
            }

        return result["payload"]

    except Exception as exc:
        return {
            "error": (
                f"{type(exc).__name__}: {str(exc)}"
            )
        }

    finally:
        if client is not None:
            try:
                client.loop_stop()
            except Exception:
                pass

            try:
                client.disconnect()
            except Exception:
                pass


# =========================================================
# SIDEBAR: CONFIGURACIÓN
# =========================================================

with st.sidebar:
    st.markdown("## `MQTT_CONFIG`")
    st.markdown("---")

    st.markdown(
        '<div style="font-family:Fira Code,monospace;'
        'font-size:12px;color:#8B949E;margin-bottom:15px;">'
        '// Parámetros de conexión'
        '</div>',
        unsafe_allow_html=True
    )

    broker = st.text_input(
        "broker_host",
        value="broker.mqttdashboard.com",
        help="Dirección del broker MQTT"
    )

    port = st.number_input(
        "broker_port",
        value=1883,
        min_value=1,
        max_value=65535,
        step=1,
        help="Puerto del broker MQTT"
    )

    topic = st.text_input(
        "subscription_topic",
        value="Sensor/THP2",
        help="Tópico al que deseas suscribirte"
    )

    client_id = st.text_input(
        "client_id",
        value="streamlit_client",
        help="Identificador único del cliente MQTT"
    )

    timeout = st.number_input(
        "timeout_seconds",
        value=8,
        min_value=1,
        max_value=60,
        step=1,
        help="Tiempo máximo de espera por un mensaje"
    )

    st.markdown("---")

    st.markdown(
        '<div style="font-family:Fira Code,monospace;'
        'font-size:12px;color:#8B949E;line-height:2;">'
        '<span style="color:#79C0FF;">PROTOCOL</span> MQTT<br>'
        '<span style="color:#79C0FF;">FORMAT</span> JSON / TEXT<br>'
        '<span style="color:#79C0FF;">TIMEOUT</span> '
        + str(int(timeout)) + ' seconds'
        + '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown("""
<div class="editor-header">
    <span class="editor-dot" style="background:#FF5F57;"></span>
    <span class="editor-dot" style="background:#FEBC2E;"></span>
    <span class="editor-dot" style="background:#28C840;"></span>
    <span class="editor-filename">sensor_reader.py</span>
</div>
<div class="editor-content">
    <div class="code-comment"># IoT / MQTT / Sensor monitoring</div>
    <div class="code-title">MQTT Sensor Reader</div>
    <div class="code-comment">
        <span class="syntax-purple">class</span>
        <span class="syntax-green"> SensorMonitor</span>:<br>
        &nbsp;&nbsp;&nbsp;&nbsp;<span class="syntax-blue">"""</span>
        Receive and inspect sensor messages.
        <span class="syntax-blue">"""</span><br>
        &nbsp;&nbsp;&nbsp;&nbsp;protocol = <span class="syntax-orange">"MQTT"</span><br>
        &nbsp;&nbsp;&nbsp;&nbsp;data_format = <span class="syntax-orange">"JSON / TEXT"</span>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# INFORMACIÓN
# =========================================================

with st.expander("README.md  |  Instrucciones de uso"):

    st.markdown("""
    **Descripción**

    Aplicación para recibir y visualizar mensajes de sensores mediante MQTT.

    **Configuración**

    1. Define la dirección del broker.
    2. Selecciona el puerto MQTT.
    3. Introduce el tópico de suscripción.
    4. Define un ID de cliente.
    5. Ejecuta la lectura para esperar un mensaje.

    **Brokers públicos de prueba**

    - `broker.mqttdashboard.com`
    - `test.mosquitto.org`
    - `broker.hivemq.com`

    **Importante:** otro dispositivo debe publicar datos en el mismo tópico.
    Conectarse al broker no garantiza que exista un mensaje disponible.
    """)


# =========================================================
# ESTADO DE CONEXIÓN
# =========================================================

# Escapar el contenido del usuario para evitar que caracteres
# HTML en el broker o tópico rompan la interfaz.
safe_broker = html.escape(str(broker))
safe_topic = html.escape(str(topic))

st.markdown(
    f"""
    <div class="status-bar">
        <span class="status-green">● READY</span>
        &nbsp; | &nbsp;
        <span>HOST:</span> {safe_broker}
        &nbsp; | &nbsp;
        <span>PORT:</span> {int(port)}
        &nbsp; | &nbsp;
        <span>TOPIC:</span> {safe_topic}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LECTURA DEL SENSOR
# =========================================================

st.markdown("### `01` — Ejecutar lectura")

st.markdown(
    '<div class="code-comment">'
    '# Connect to broker, subscribe and receive the next message.'
    '</div>',
    unsafe_allow_html=True
)

if st.button(
    "▶  EJECUTAR LECTURA",
    use_container_width=True
):
    if not broker.strip() or not topic.strip() or not client_id.strip():
        st.session_state.sensor_data = {
            "error": "El broker, el tópico y el ID del cliente son obligatorios."
        }
        st.session_state.last_read_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else:
        with st.spinner(
            "Conectando al broker MQTT y esperando datos..."
        ):
            sensor_data = get_mqtt_message(
                broker=broker,
                port=int(port),
                topic=topic,
                client_id=client_id,
                timeout=int(timeout)
            )

            st.session_state.sensor_data = sensor_data
            st.session_state.last_read_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )


# =========================================================
# RESULTADOS
# =========================================================

if st.session_state.sensor_data is not None:

    st.markdown("---")
    st.markdown("### `02` — Output / Sensor data")

    data = st.session_state.sensor_data

    if isinstance(data, dict) and "error" in data:

        st.error(f"CONNECTION_ERROR: {data['error']}")

        st.markdown(
            '<div class="status-bar">'
            '<span class="status-red">● ERROR</span>'
            '&nbsp; | &nbsp; No se pudo completar la lectura.'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="status-bar">'
            '<span class="status-green">● MESSAGE_RECEIVED</span>'
            '&nbsp; | &nbsp; Lectura recibida correctamente.'
            '</div>',
            unsafe_allow_html=True
        )

        if st.session_state.last_read_time:
            st.caption(
                "Timestamp: "
                + st.session_state.last_read_time
            )

        if isinstance(data, dict):

            st.markdown("#### `payload`")

            items = list(data.items())

            if not items:
                st.info(
                    "El mensaje recibido es un objeto JSON vacío: {}"
                )

            for start in range(0, len(items), 3):
                group = items[start:start + 3]
                cols = st.columns(len(group))

                for col, (key, value) in zip(cols, group):
                    if isinstance(value, (dict, list)):
                        display_value = json.dumps(
                            value,
                            ensure_ascii=False
                        )
                    elif value is None:
                        display_value = "null"
                    elif isinstance(value, bool):
                        display_value = str(value)
                    else:
                        display_value = str(value)

                    with col:
                        st.metric(
                            label=str(key),
                            value=display_value
                        )

            with st.expander("payload.json  |  JSON completo"):
                st.json(data)

            with st.expander("payload.raw  |  Texto serializado"):
                st.code(
                    json.dumps(
                        data,
                        indent=4,
                        ensure_ascii=False,
                        default=str
                    ),
                    language="json"
                )

        elif isinstance(data, list):

            st.markdown("#### `payload.array`")
            st.json(data)

            with st.expander("payload.raw  |  Texto serializado"):
                st.code(
                    json.dumps(
                        data,
                        indent=4,
                        ensure_ascii=False,
                        default=str
                    ),
                    language="json"
                )

        else:

            st.markdown("#### `payload.text`")
            st.code(str(data), language="text")


# =========================================================
# PIE DE PÁGINA
# =========================================================

st.markdown("""
<div class="footer">
    MQTT SENSOR READER // IOT DEBUGGING CONSOLE // v1.1
</div>
""", unsafe_allow_html=True)

