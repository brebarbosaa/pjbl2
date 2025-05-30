# controllers/app_controller.py
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
import json
from models.db import db, instance
from flask import current_app
from flask_login import LoginManager

# Importar seus Blueprints
from controllers.user_controller import user
from controllers.sensors_controller import sensor_
from controllers.actuators_controller import actuator_
from controllers.reads_controller import read
from controllers.writes_controller import write
from models.iot.read import Read
from models.iot.sensors import Sensor
from models.iot.actuators import Actuator
from models.iot.write import Write
from models.users.user_model import User

temperature = 0
humidity = 0
nivel_racao = ""
movimento = ""

socketio = SocketIO(cors_allowed_origins="*")
mqtt_client = Mqtt()
topics = [
    "sensor/temperatura",
    "sensor/umidade",
    "sensor/nivel_racao",
    "sensor/movimento"
]

def create_app():
    app = Flask(__name__,
                template_folder="./templates/",
                static_folder="./static/",
                root_path="./")
    #app.config['SECRET_KEY'] = 'admin123@@'

    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)

    # MQTT config
    app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''
    app.config['MQTT_PASSWORD'] = ''
    app.config['MQTT_KEEPALIVE'] = 60
    app.config['MQTT_TLS_ENABLED'] = False

    mqtt_client.init_app(app)
    socketio.init_app(app)

    with app.app_context():
        atuadores = Actuator.query.all()
        for a in atuadores:
            if a.topic_subscribe:
                print(f"[MQTT] Subscrito no tópico: {a.topic_subscribe}")
                mqtt_client.subscribe(a.topic_subscribe)


    # Register Blueprints
    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(sensor_, url_prefix='/')
    app.register_blueprint(actuator_, url_prefix='/')
    app.register_blueprint(read, url_prefix='/')
    app.register_blueprint(write, url_prefix='/')

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        return render_template("base_login.html")

    @app.route('/logoff')
    def logoff():
        return render_template("login.html")

    @app.route('/home')
    def home():
        user = session.get('user')
        is_admin = session.get('is_admin', False)
        return render_template('home.html', user=user, is_admin=is_admin)

    @app.route('/tempo_real')
    def tempo_real():
        values = {
            "temperature": temperature,
            "humidity": humidity,
            "nivel_racao": nivel_racao,
            "movimento": movimento
        }
        socketio.emit('update_values', values)
        return render_template("tr.html", values=values)

    @app.route('/publish')
    def publish():
        return render_template('publish.html')

    @app.route('/publish_message', methods=['POST'])
    def publish_message():
        request_data = request.get_json()
        topic = request_data['topic']
        message = request_data['message']
        try:
            mqtt_client.publish(topic, message)

            # Gravar no banco como comando manual
            with current_app.app_context():
                print(f"[DEBUG] Publicando no tópico {topic} com mensagem: {message}")
                actuator = Actuator.query.filter_by(topic=topic).first()
                if not actuator:
                    print("[ERRO] Atuador não encontrado para esse tópico")
                if actuator:
                    Write.save_write(actuator, message, origin="manual")

            return json.dumps({"status": "Mensagem publicada com sucesso!"}), 200
        except Exception as e:
            print("Erro ao publicar:", str(e))
            return json.dumps({"status": "Erro ao publicar mensagem"}), 500

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
        global temperature, humidity, nivel_racao, movimento

        topic = message.topic
        payload = message.payload.decode()
        print(f"[DEBUG] Mensagem recebida | Tópico: {topic} | Conteúdo: {payload}")

        # Atualizar dados para tempo real
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
        elif topic == "sensor/nivel_racao":
            nivel_racao = payload
        elif topic == "sensor/movimento":
            movimento = payload

        socketio.emit('update_values', {
            "temperature": temperature,
            "humidity": humidity,
            "nivel_racao": nivel_racao,
            "movimento": movimento
        })

        # Salvar leitura ou atuação automática
        with app.app_context():
            try:
                print(f"[DEBUG] Verificando tópico recebido: {topic}")
                all_actuators = Actuator.query.all()
                for a in all_actuators:
                    device_name = a.device.name if a.device else 'Desconhecido'
                    print(f"[DEBUG] Atuador {device_name} | topic: {a.topic} | topic_subscribe: {a.topic_subscribe}")

                sensor = Sensor.query.filter_by(topic=topic).first()
                if sensor:
                    try:
                        number_str = payload.split()[0]
                        value = float(number_str)
                    except (ValueError, IndexError):
                        value = payload
                    Read.save_read(sensor, value)
                else:

                    print(f"[DEBUG] Tópico recebido: {repr(topic)}")
                    actuator = Actuator.query.filter(
                        (Actuator.topic == topic) | (Actuator.topic_subscribe == topic)
                    ).first()
                    for a in all_actuators:
                        print(
                            f"[DEBUG] Atuador {a.id} | topic: {repr(a.topic)} | topic_subscribe: {repr(a.topic_subscribe)}")

                    if actuator:
                        device_name = actuator.device.name if actuator.device else 'Desconhecido'
                        print(f"[DEBUG] Atuador encontrado: {device_name}")
                        origin = "manual" if topic == actuator.topic else "automatico"
                        Write.save_write(actuator, payload, origin=origin)
                    else:
                        print(f"[DEBUG] Atuador encontrado: Nenhum")
            except Exception as e:
                print("[ERRO] Falha ao processar mensagem MQTT:", str(e))

    return app
