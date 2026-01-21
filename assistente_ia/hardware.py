import platform

# Verifica se estamos rodando num PC ou no Raspberry Pi
SISTEMA = platform.system()
ARQUITETURA = platform.machine()

# Tenta importar a biblioteca de pinos. Se falhar, é porque estamos no PC.
try:
    import RPi.GPIO as GPIO
    MODO_SIMULACAO = False
    print("🔌 Hardware Real Detectado (Raspberry Pi)")
except ImportError:
    MODO_SIMULACAO = True
    print("💻 Modo Simulação Ativado (PC Ubuntu)")

class ControleHardware:
    def __init__(self):
        if not MODO_SIMULACAO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(17, GPIO.OUT) # Exemplo: LED no pino 17

    def ligar_luz(self):
        if MODO_SIMULACAO:
            print("[SIMULAÇÃO] 💡 A luz foi LIGADA virtualmente.")
        else:
            GPIO.output(17, GPIO.HIGH)
            print("[HARDWARE] Luz ligada no pino 17.")

    def desligar_luz(self):
        if MODO_SIMULACAO:
            print("[SIMULAÇÃO] 🌑 A luz foi DESLIGADA virtualmente.")
        else:
            GPIO.output(17, GPIO.LOW)
            print("[HARDWARE] Luz desligada.")