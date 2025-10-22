# Documentação do Código da Assistente de Bordo com IA para Raspberry Pi 5

## 1. Introdução

Este documento detalha a estrutura e as funcionalidades simuladas da assistente de bordo com inteligência artificial, projetada para rodar em um Raspberry Pi 5. O código `ai_assistant_raspberry_pi_simulator.py` demonstra a integração de diversas capacidades, como interface de voz, controle de veículos, base de conhecimento, visão computacional, aprendizado de máquina e processamento de dados do ESP32.

## 2. Visão Geral do Código

O simulador da assistente de bordo é composto por várias classes, cada uma encapsulando uma funcionalidade específica:

*   **`VoiceInterface`:** Simula a interação por voz (escuta e fala).
*   **`VehicleControl`:** Simula o controle de funções do veículo (luzes, Spotify, GPS, câmeras).
*   **`KnowledgeBase`:** Armazena e responde a perguntas sobre mecânica e informações gerais.
*   **`ComputerVision`:** Simula a detecção de semáforos e reconhecimento de veículos.
*   **`MachineLearningModule`:** Simula o aprendizado de preferências do usuário, análise de padrões de condução e previsão de falhas.
*   **`DataProcessor`:** Recebe e gerencia os logs de dados do ESP32.
*   **`AI_Assistant`:** A classe principal que integra todas as funcionalidades e orquestra a interação.

## 3. Detalhes da Implementação

### 3.1. `VoiceInterface`

Esta classe simula a capacidade da assistente de ouvir comandos do motorista e responder verbalmente. Em uma implementação real, utilizaria APIs de reconhecimento de fala (ASR) e síntese de fala (TTS).

```python
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
```

### 3.2. `VehicleControl`

Gerencia as interações com os sistemas do veículo, como ligar/desligar faróis, controlar o Spotify, obter localização GPS e manipular câmeras. Em um sistema real, isso envolveria comunicação via CAN Bus ou GPIOs.

```python
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
```

### 3.3. `KnowledgeBase`

Contém informações pré-definidas sobre mecânica automotiva e conhecimentos gerais, permitindo que a assistente responda a perguntas do motorista. Em uma aplicação real, poderia ser integrada a grandes modelos de linguagem (LLMs) para respostas mais dinâmicas e abrangentes.

```python
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
```

### 3.4. `ComputerVision`

Simula a capacidade de processar imagens de câmeras para detectar objetos como semáforos e outros veículos. Em uma implementação real, utilizaria bibliotecas como OpenCV e modelos de *deep learning*.

```python
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
```

### 3.5. `MachineLearningModule`

Este módulo simula o aprendizado e adaptação da assistente. Inclui funções para aprender preferências do usuário, analisar padrões de condução e prever falhas com base nos dados do motor. Em um sistema real, envolveria modelos de ML treinados com grandes volumes de dados.

```python
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
```

### 3.6. `DataProcessor`

Responsável por receber e armazenar os logs de dados enviados pelo ESP32. Em uma implementação real, garantiria a integridade e o processamento eficiente desses dados para uso pelos outros módulos da assistente.

```python
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
```

### 3.7. `AI_Assistant`

A classe principal que integra todas as funcionalidades. Ela inicializa os módulos, processa comandos de voz e executa tarefas em segundo plano, como a visão computacional e a previsão de falhas. A comunicação com o ESP32 é simulada através de uma thread separada (`esp32_data_stream`).

```python
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
```

## 4. Considerações para Implementação Real

*   **Hardware:** O Raspberry Pi 5 oferece poder de processamento suficiente para as tarefas de IA, mas a escolha de periféricos (microfones, câmeras de alta resolução, telas) é crucial.
*   **Software de Voz:** Integração com serviços de ASR/TTS de alta qualidade para reconhecimento e síntese de fala natural.
*   **Modelos de IA:** Utilização de modelos de *machine learning* e *deep learning* pré-treinados ou treinados especificamente para o contexto automotivo para visão computacional, processamento de linguagem natural e previsão de falhas.
*   **Conectividade:** Gerenciamento robusto de conectividade (Wi-Fi, Bluetooth, 4G/5G) para serviços online (Spotify, mapas) e garantia de funcionalidade offline.
*   **Segurança Cibernética:** Proteção contra acessos não autorizados e vulnerabilidades, especialmente considerando a integração com sistemas críticos do veículo.
*   **Interface do Usuário:** Desenvolvimento de uma interface gráfica intuitiva para a tela, complementando a interação por voz.

## 5. Próximos Passos

O próximo passo seria aprofundar na integração real dos módulos, desenvolvendo as APIs de comunicação entre o Raspberry Pi e os periféricos do veículo, bem como a implementação dos modelos de IA e a interface de usuário final. A comunicação robusta com o ESP32 também seria um ponto chave.
