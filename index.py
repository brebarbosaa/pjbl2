from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from sensors import sensors
from user import user
from actuators import actuators
from erros import erros_bp
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import json

temperature = 0
humidity = 0
nivel_agua = ""
movimento = ""

app = Flask(__name__)

app.config['SECRET_KEY'] = 'admin123@@'

app.register_blueprint(user, url_prefix='/')
app.register_blueprint(sensors, url_prefix='/')
app.register_blueprint(actuators, url_prefix='/')
app.register_blueprint(erros_bp, url_prefix='/')

# Config MQTT
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

mqtt_client = Mqtt()
mqtt_client.init_app(app)

# Lista de tópicos esperados do ESP32
topics = [
    "sensor/temperatura",
    "sensor/umidade",
    "sensor/nivel_agua",
    "sensor/movimento"
]

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/logoff')
def logoff():
    return render_template("login.html")

@app.route('/home')
def home():
    user = session.get('user')  # ou como você armazena o login
    is_admin = session.get('is_admin', False)  # ou outro controle que você tenha
    return render_template('home.html', user=user, is_admin=is_admin)


@app.route('/tempo_real')
def tempo_real():
    global temperature, humidity, nivel_agua, movimento
    values = {
        "temperature": temperature,
        "humidity": humidity,
        "nivel_agua": nivel_agua,
        "movimento": movimento
    }
    return render_template("tr.html", values=values)

@app.route('/publish')
def publish():
    return render_template('publish.html')

@app.route('/publish_message', methods=['GET', 'POST'])
def publish_message():
    request_data = request.get_json()
    publish_result = mqtt_client.publish(request_data['topic'], request_data['message'])
    return jsonify(publish_result)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Broker conectado com sucesso!')
        for t in topics:
            mqtt_client.subscribe(t)
    else:
        print('Erro na conexão. Código:', rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    global temperature, humidity, nivel_agua, movimento
    payload = message.payload.decode()
    topic = message.topic

    print(f"Mensagem recebida | Tópico: {topic} | Conteúdo: {payload}")

    if topic == "sensor/temperatura":
        try:
            temperature = float(payload)
        except ValueError:
            temperature = 0
    elif topic == "sensor/umidade":
        try:
            humidity = float(payload)
        except ValueError:
            humidity = 0
    elif topic == "sensor/nivel_agua":
        nivel_agua = payload
    elif topic == "sensor/movimento":
        movimento = payload

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
