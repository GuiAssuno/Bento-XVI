"""
Módulo de Visão Computacional
Simula a capacidade de processar imagens de câmeras
"""

import random

class ComputerVision:
    def __init__(self):
        print("Visão Computacional: Inicializada.")

    def detect_traffic_light(self):
        """Simula a detecção de semáforos."""
        return random.choice([
            "Semáforo: Verde", 
            "Semáforo: Amarelo", 
            "Semáforo: Vermelho", 
            "Semáforo: Não detectado"
        ])

    def recognize_vehicles(self):
        """Simula o reconhecimento de outros veículos."""
        vehicles = [
            "Carro à frente", 
            "Moto à direita", 
            "Caminhão à esquerda", 
            "Nenhum veículo próximo"
        ]
        return random.choice(vehicles)

