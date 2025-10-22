"""
Módulo de Interface de Voz
Simula a capacidade de ouvir comandos e responder verbalmente
"""

import random

class VoiceInterface:
    def __init__(self):
        print("Interface de Voz: Inicializada.")

    def listen(self):
        """Simula a escuta de comandos de voz."""
        commands = [
            "Qual a temperatura do motor?", 
            "Tocar Spotify", 
            "Onde fica o posto mais próximo?", 
            "O que é um carburador?", 
            "Ligar faróis", 
            "Parar música"
        ]
        return random.choice(commands)

    def speak(self, text):
        """Simula a resposta de voz."""
        print(f"Assistente de Bordo (Voz): {text}")
        return text

