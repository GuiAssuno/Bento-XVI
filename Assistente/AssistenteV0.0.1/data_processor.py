"""
Módulo de Processamento de Dados
Responsável por receber e armazenar os logs de dados do ESP32
"""

class DataProcessor:
    def __init__(self):
        print("Processador de Dados: Inicializado.")
        self.esp32_logs = []

    def receive_esp32_log(self, log):
        """Recebe e armazena logs do ESP32"""
        self.esp32_logs.append(log)
        if len(self.esp32_logs) > 100:
            self.esp32_logs.pop(0)

    def get_latest_motor_data(self):
        """Retorna os dados mais recentes do motor"""
        if self.esp32_logs:
            return self.esp32_logs[-1]['sensor_data']
        return {}

