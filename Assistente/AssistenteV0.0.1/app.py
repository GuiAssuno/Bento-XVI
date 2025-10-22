"""
Aplicação Flask para a Assistente de Bordo do Opala 4.1
Backend principal que expõe APIs REST para o frontend
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import threading
import time
import os

# Importar módulos da assistente
from modules.voice_interface import VoiceInterface
from modules.vehicle_control import VehicleControl
from modules.knowledge_base import KnowledgeBase
from modules.computer_vision import ComputerVision
from modules.machine_learning import MachineLearningModule
from modules.data_processor import DataProcessor

app = Flask(__name__, 
            static_folder='../frontend/static',
            template_folder='../frontend/templates')
CORS(app)  # Habilitar CORS para permitir requisições do frontend

# Instância global da assistente
assistente = None

class AssistenteBordoBackend:
    def __init__(self):
        self.voice_interface = VoiceInterface()
        self.vehicle_control = VehicleControl()
        self.knowledge_base = KnowledgeBase()
        self.computer_vision = ComputerVision()
        self.ml_module = MachineLearningModule()
        self.data_processor = DataProcessor()
        self.running = False
        print("Assistente de Bordo Backend: Inicializada.")

    def process_command(self, command):
        """Processa comandos de voz ou texto"""
        response = "Desculpe, não entendi seu comando."
        
        if "temperatura do motor" in command.lower():
            motor_data = self.data_processor.get_latest_motor_data()
            temp = motor_data.get("temperatura_motor_ect", "desconhecida")
            response = f"A temperatura atual do motor é de {temp}°C."
        elif "spotify" in command.lower() or "música" in command.lower() or "tocar" in command.lower():
            response = self.vehicle_control.toggle_spotify()
        elif "posto" in command.lower():
            response = f"Buscando posto mais próximo de {self.vehicle_control.get_gps_location()}..."
        elif "carburador" in command.lower() or "injeção" in command.lower():
            response = self.knowledge_base.query_mechanics(command)
        elif "faróis" in command.lower() or "farol" in command.lower() or "luz" in command.lower():
            response = self.vehicle_control.toggle_lights()
        elif "câmera" in command.lower():
            response = self.vehicle_control.control_camera("gravar")
        elif "parar" in command.lower() and "música" in command.lower():
            if self.vehicle_control.spotify_playing:
                self.vehicle_control.toggle_spotify()
                response = "Spotify pausado."
            else:
                response = "Spotify já está pausado."
        elif "menu" in command.lower() or "funcionalidades" in command.lower():
            response = "Abrindo menu de funcionalidades..."
        
        return response

    def get_motor_data(self):
        """Retorna dados do motor"""
        return self.data_processor.get_latest_motor_data()

    def get_vehicle_status(self):
        """Retorna status geral do veículo"""
        motor_data = self.data_processor.get_latest_motor_data()
        return {
            "lights_on": self.vehicle_control.lights_on,
            "spotify_playing": self.vehicle_control.spotify_playing,
            "motor_data": motor_data,
            "gps_location": self.vehicle_control.get_gps_location()
        }

    def start_background_tasks(self):
        """Inicia tarefas de fundo"""
        self.running = True
        
        def background_loop():
            while self.running:
                # Simula a detecção visual
                traffic_light_status = self.computer_vision.detect_traffic_light()
                vehicle_recognition = self.computer_vision.recognize_vehicles()
                
                # Simula a previsão de falhas
                motor_data = self.data_processor.get_latest_motor_data()
                if motor_data:
                    failure_prediction = self.ml_module.predict_failure(motor_data)
                    if "Alerta" in failure_prediction:
                        print(f"[ALERTA] {failure_prediction}")
                
                time.sleep(5)
        
        thread = threading.Thread(target=background_loop)
        thread.daemon = True
        thread.start()

# Rotas da API

@app.route('/')
def index():
    """Serve a página principal"""
    return send_from_directory('../frontend/templates', 'index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    """Retorna o status geral do veículo"""
    if assistente:
        status = assistente.get_vehicle_status()
        return jsonify(status)
    return jsonify({"error": "Assistente não inicializada"}), 500

@app.route('/api/motor', methods=['GET'])
def get_motor():
    """Retorna dados do motor"""
    if assistente:
        motor_data = assistente.get_motor_data()
        return jsonify(motor_data)
    return jsonify({"error": "Assistente não inicializada"}), 500

@app.route('/api/command', methods=['POST'])
def process_command():
    """Processa um comando de voz ou texto"""
    if assistente:
        data = request.get_json()
        command = data.get('command', '')
        response = assistente.process_command(command)
        return jsonify({"response": response})
    return jsonify({"error": "Assistente não inicializada"}), 500

@app.route('/api/lights', methods=['POST'])
def toggle_lights():
    """Liga/desliga os faróis"""
    if assistente:
        response = assistente.vehicle_control.toggle_lights()
        return jsonify({"response": response, "lights_on": assistente.vehicle_control.lights_on})
    return jsonify({"error": "Assistente não inicializada"}), 500

@app.route('/api/music', methods=['POST'])
def toggle_music():
    """Liga/desliga o Spotify"""
    if assistente:
        response = assistente.vehicle_control.toggle_spotify()
        return jsonify({"response": response, "spotify_playing": assistente.vehicle_control.spotify_playing})
    return jsonify({"error": "Assistente não inicializada"}), 500

@app.route('/api/camera', methods=['GET'])
def get_camera():
    """Retorna dados da visão computacional"""
    if assistente:
        traffic_light = assistente.computer_vision.detect_traffic_light()
        vehicles = assistente.computer_vision.recognize_vehicles()
        return jsonify({
            "traffic_light": traffic_light,
            "vehicles": vehicles
        })
    return jsonify({"error": "Assistente não inicializada"}), 500

@app.route('/api/gps', methods=['GET'])
def get_gps():
    """Retorna localização GPS"""
    if assistente:
        location = assistente.vehicle_control.get_gps_location()
        return jsonify({"location": location})
    return jsonify({"error": "Assistente não inicializada"}), 500

# Simulação de dados do ESP32 (em uma thread separada)
def esp32_data_stream():
    """Simula o stream de dados do ESP32"""
    import sys
    sys.path.append('/home/ubuntu')
    from esp32_injection_simulator import read_sensors, calculate_injection
    
    while True:
        if assistente:
            sensor_data = read_sensors()
            injection_time = calculate_injection(sensor_data)
            log_entry = {
                "timestamp": time.time(),
                "sensor_data": sensor_data,
                "injection_time_ms": injection_time,
                "status": "OK"
            }
            assistente.data_processor.receive_esp32_log(log_entry)
        time.sleep(0.1)

def init_assistente():
    """Inicializa a assistente e as threads de fundo"""
    global assistente
    assistente = AssistenteBordoBackend()
    assistente.start_background_tasks()
    
    # Inicia o stream de dados do ESP32
    esp32_thread = threading.Thread(target=esp32_data_stream)
    esp32_thread.daemon = True
    esp32_thread.start()
    
    print("Assistente de Bordo: Sistema inicializado com sucesso!")

if __name__ == '__main__':
    init_assistente()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

