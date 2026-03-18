from hardware import ControleHardware
from cerebro import perguntar_ia

# Inicializa o hardware
casa = ControleHardware()

def processar_comando(texto):
    texto = texto.lower()
    
    # Lógica de comando antes de chamar lola
    if "ligar luz" in texto:
        casa.ligar_luz()
        return "Liguei a luz para você."
    elif "desligar luz" in texto:
        casa.desligar_luz()
        return "Desliguei a luz."
    else:
        # Se não for comando simples, pergunta pro cerebro.py
        return perguntar_ia(texto)

# ========================= Teste  ===========================
if __name__ == "__main__":
    while True:
        comando = input("Você: ")
        resposta = processar_comando(comando)
        print(f"Assistente: {resposta}")
