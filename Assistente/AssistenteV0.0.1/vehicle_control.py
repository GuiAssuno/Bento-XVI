"""
Módulo de Controle do Veículo
Gerencia as interações com os sistemas do veículo
"""

class VehicleControl:
    def __init__(self):
        print("Controle do Veículo: Inicializado.")
        self.lights_on = False
        self.spotify_playing = False

    def toggle_lights(self):
        """Liga/desliga os faróis"""
        self.lights_on = not self.lights_on
        status = "ligados" if self.lights_on else "desligados"
        return f"Faróis {status}."

    def toggle_spotify(self):
        """Liga/desliga o Spotify"""
        self.spotify_playing = not self.spotify_playing
        status = "tocando" if self.spotify_playing else "pausado"
        return f"Spotify {status}."

    def get_gps_location(self):
        """Simula a obtenção da localização GPS."""
        return "Latitude: -23.5505, Longitude: -46.6333 (São Paulo)"

    def control_camera(self, action):
        """Simula o controle de câmeras."""
        return f"Câmera: Ação '{action}' executada."

