import time
import random
import threading

class VoiceInterface:
    def __init__(self):
        print("Interface de Voz: Inicializada.")

    def listen(self):
        """Simula a escuta de comandos de voz."""
        commands = ["Qual a temperatura do motor?", "Tocar Spotify", "Onde fica o posto mais próximo?", "O que é um carburador?", "Ligar faróis", "Parar música"]
        return random.choice(commands)

    def speak(self, text):
        """Simula a resposta de voz."""
        print(f"Assistente de Bordo (Voz): {text}")

class VehicleControl:
    def __init__(self):
        print("Controle do Veículo: Inicializado.")
        self.lights_on = False
        self.spotify_playing = False

    def toggle_lights(self):
        self.lights_on = not self.lights_on
        status = "ligados" if self.lights_on else "desligados"
        return f"Faróis {status}."

    def toggle_spotify(self):
        self.spotify_playing = not self.spotify_playing
        status = "tocando" if self.spotify_playing else "pausado"
        return f"Spotify {status}."

    def get_gps_location(self):
        """Simula a obtenção da localização GPS."""
        return "Latitude: -23.5505, Longitude: -46.6333 (São Paulo)"

    def control_camera(self, action):
        """Simula o controle de câmeras."""
        return f"Câmera: Ação '{action}' executada."

class KnowledgeBase:
    def __init__(self):
        print("Base de Conhecimento: Inicializada.")
        self.mechanics_data = {
            "carburador": "Um carburador é um dispositivo que mistura ar e combustível em proporções adequadas para a combustão interna de um motor.",
            "injeção eletrônica": "A injeção eletrônica é um sistema que controla eletronicamente a quantidade de combustível injetada no motor, otimizando a combustão."
        }
        self.general_data = {
            "temperatura do motor": "A temperatura ideal do motor varia, mas geralmente fica entre 90°C e 105°C."
        }

    def query_mechanics(self, query):
        return self.mechanics_data.get(query.lower(), "Não encontrei informações específicas sobre mecânica para esta pergunta.")

    def query_general(self, query):
        return self.general_data.get(query.lower(), "Não encontrei informações gerais para esta pergunta.")

class ComputerVision:
    def __init__(self):
        print("Visão Computacional: Inicializada.")

    def detect_traffic_light(self):
        """Simula a detecção de semáforos."""
        return random.choice(["Semáforo: Verde", "Semáforo: Amarelo", "Semáforo: Vermelho", "Semáforo: Não detectado"])

    def recognize_vehicles(self):
        """Simula o reconhecimento de outros veículos."""
        vehicles = ["Carro à frente", "Moto à direita", "Caminhão à esquerda", "Nenhum veículo próximo"]
        return random.choice(vehicles)

class MachineLearningModule:
    def __init__(self):
        print("Módulo de Machine Learning: Inicializado.")
        self.user_preferences = {}
        self.driving_patterns = []

    def learn_preferences(self, user_id, preference, value):
        self.user_preferences[user_id] = self.user_preferences.get(user_id, {})
        self.user_preferences[user_id][preference] = value
        return f"Preferência '{preference}' definida para '{value}'."

    def analyze_driving_pattern(self, speed, rpm, fuel_consumption):
        self.driving_patterns.append({"speed": speed, "rpm": rpm, "fuel_consumption": fuel_consumption})
        if len(self.driving_patterns) > 100: # Manter um histórico limitado
            self.driving_patterns.pop(0)
        return "Padrão de condução analisado."

    def predict_failure(self, motor_data):
        """Simula a previsão de falhas com base em dados do motor."""
        if motor_data.get("temperatura_motor_ect", 0) > 100 and random.random() < 0.3:
            return "Alerta: Possível superaquecimento do motor detectado!"
        return "Nenhuma falha iminente detectada."

class DataProcessor:
    def __init__(self):
        print("Processador de Dados: Inicializado.")
        self.esp32_logs = []

    def receive_esp32_log(self, log):
        self.esp32_logs.append(log)
        if len(self.esp32_logs) > 100: # Manter um histórico limitado
            self.esp32_logs.pop(0)
        # print(f"Dados do ESP32 recebidos: {log['sensor_data']}")

    def get_latest_motor_data(self):
        if self.esp32_logs:
            return self.esp32_logs[-1]['sensor_data']
        return {}

class AI_Assistant:
    def __init__(self):
        self.voice_interface = VoiceInterface()
        self.vehicle_control = VehicleControl()
        self.knowledge_base = KnowledgeBase()
        self.computer_vision = ComputerVision()
        self.ml_module = MachineLearningModule()
        self.data_processor = DataProcessor()
        print("Assistente de Bordo com IA: Inicializada.")

    def process_command(self, command):
        response = "Desculpe, não entendi seu comando."
        if "temperatura do motor" in command.lower():
            motor_data = self.data_processor.get_latest_motor_data()
            temp = motor_data.get("temperatura_motor_ect", "desconhecida")
            response = f"A temperatura atual do motor é de {temp}°C."
        elif "spotify" in command.lower():
            response = self.vehicle_control.toggle_spotify()
        elif "posto mais próximo" in command.lower():
            response = f"Buscando posto mais próximo de {self.vehicle_control.get_gps_location()}..."
        elif "carburador" in command.lower() or "injeção eletrônica" in command.lower():
            response = self.knowledge_base.query_mechanics(command)
        elif "faróis" in command.lower():
            response = self.vehicle_control.toggle_lights()
        elif "câmera" in command.lower():
            response = self.vehicle_control.control_camera("gravar") # Exemplo
        elif "parar música" in command.lower():
            if self.vehicle_control.spotify_playing:
                self.vehicle_control.toggle_spotify()
                response = "Spotify pausado."
            else:
                response = "Spotify já está pausado."
        return response

    def run_background_tasks(self):
        while True:
            # Simula a detecção visual
            traffic_light_status = self.computer_vision.detect_traffic_light()
            vehicle_recognition = self.computer_vision.recognize_vehicles()
            # print(f"[Visão Computacional] {traffic_light_status}, {vehicle_recognition}")

            # Simula a previsão de falhas
            motor_data = self.data_processor.get_latest_motor_data()
            if motor_data:
                failure_prediction = self.ml_module.predict_failure(motor_data)
                if "Alerta" in failure_prediction:
                    self.voice_interface.speak(failure_prediction)

            time.sleep(5) # Executa tarefas de fundo a cada 5 segundos

    def start(self):
        # Inicia tarefas de fundo em uma thread separada
        background_thread = threading.Thread(target=self.run_background_tasks)
        background_thread.daemon = True # Permite que a thread seja encerrada com o programa principal
        background_thread.start()

        print("Assistente de Bordo: Pronta para interação.")
        while True:
            command = self.voice_interface.listen()
            print(f"Motorista: {command}")
            response = self.process_command(command)
            self.voice_interface.speak(response)
            time.sleep(2) # Simula tempo de processamento e resposta

# Simulação de dados do ESP32 (em uma thread separada para não bloquear a assistente)
def esp32_data_stream(data_processor):
    from esp32_injection_simulator import read_sensors, calculate_injection
    while True:
        sensor_data = read_sensors()
        injection_time = calculate_injection(sensor_data)
        log_entry = {
            "timestamp": time.time(),
            "sensor_data": sensor_data,
            "injection_time_ms": injection_time,
            "status": "OK"
        }
        data_processor.receive_esp32_log(log_entry)
        time.sleep(0.1) # Envia dados a cada 100ms

if __name__ == "__main__":
    assistant = AI_Assistant()

    # Inicia o stream de dados do ESP32 em uma thread separada
    esp32_thread = threading.Thread(target=esp32_data_stream, args=(assistant.data_processor,))
    esp32_thread.daemon = True
    esp32_thread.start()

    assistant.start()

