"""
Módulo de Machine Learning
Simula o aprendizado e adaptação da assistente
"""

import random

class MachineLearningModule:
    def __init__(self):
        print("Módulo de Machine Learning: Inicializado.")
        self.user_preferences = {}
        self.driving_patterns = []

    def learn_preferences(self, user_id, preference, value):
        """Aprende preferências do usuário"""
        self.user_preferences[user_id] = self.user_preferences.get(user_id, {})
        self.user_preferences[user_id][preference] = value
        return f"Preferência '{preference}' definida para '{value}'."

    def analyze_driving_pattern(self, speed, rpm, fuel_consumption):
        """Analisa padrões de condução"""
        self.driving_patterns.append({
            "speed": speed, 
            "rpm": rpm, 
            "fuel_consumption": fuel_consumption
        })
        if len(self.driving_patterns) > 100:
            self.driving_patterns.pop(0)
        return "Padrão de condução analisado."

    def predict_failure(self, motor_data):
        """Simula a previsão de falhas com base em dados do motor."""
        if motor_data.get("temperatura_motor_ect", 0) > 100 and random.random() < 0.3:
            return "Alerta: Possível superaquecimento do motor detectado!"
        return "Nenhuma falha iminente detectada."

