import platform

# Verifica se roda num PC ou no Raspberry
SISTEMA = platform.system()
ARQUITETURA = platform.machine()

 
try: #importar a biblioteca de pinos.
    import RPi.GPIO as GPIO
    MODO_SIMULACAO = False
    
except ImportError: # Se falhar, é porque está no PC.
    MODO_SIMULACAO = True

class ControleHardware:
    def __init__(self):
        if not MODO_SIMULACAO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(17, GPIO.OUT) 

    def ligar_luz(self):
        if MODO_SIMULACAO:
            print("foi ligada")
        else:
            GPIO.output(17, GPIO.HIGH)
            print("Luz ligada no pino 17.")

    def desligar_luz(self):
        if MODO_SIMULACAO:
            print("A luz desligou.")
        else:
            GPIO.output(17, GPIO.LOW)
            print("Luz desligada.")
