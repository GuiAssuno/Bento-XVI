import platform

# Verifica se roda num PC ou no Raspberry
SISTEMA = platform.system()
ARQUITETURA = platform.machine()

 
try: #importar a biblioteca de pinos.
    import RPi.GPIO as GPIO
    MODO_SIMULACAO = False
    print("🔌 Hardware Real Detectado (Raspberry Pi)")
    
except ImportError: # Se falhar, é porque estamos no PC.
    MODO_SIMULACAO = True
    print("💻 Modo Simulação Ativado (PC Ubuntu)")

class ControleHardware:
    def __init__(self):
        if not MODO_SIMULACAO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(17, GPIO.OUT) 

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
