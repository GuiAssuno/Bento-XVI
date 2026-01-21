from hardware import ControleHardware
from cerebro import perguntar_ia

# Inicializa o hardware (Real ou Simulado)
casa = ControleHardware()

def processar_comando(texto):
    texto = texto.lower()
    
    # Lógica simples de comando antes de chamar a IA pesada
    if "ligar luz" in texto:
        casa.ligar_luz()
        return "Liguei a luz para você."
    elif "desligar luz" in texto:
        casa.desligar_luz()
        return "Desliguei a luz."
    else:
        # Se não for comando simples, pergunta pro Cérebro
        return perguntar_ia(texto)

# Teste manual no terminal
if __name__ == "__main__":
    while True:
        comando = input("Você: ")
        resposta = processar_comando(comando)
        print(f"Assistente: {resposta}")