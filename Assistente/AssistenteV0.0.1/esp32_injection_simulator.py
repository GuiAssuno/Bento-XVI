import time
import random

def read_sensors():
    """Simula a leitura de dados dos sensores do motor."""
    data = {
        "sonda_lambda": round(random.uniform(0.1, 0.9), 2),  # Tensão em Volts
        "temperatura_motor_ect": round(random.uniform(70.0, 100.0), 1),  # Graus Celsius
        "posicao_borboleta_tps": round(random.uniform(0.0, 100.0), 1),  # Percentual
        "pressao_coletor_map": round(random.uniform(30.0, 100.0), 1),  # kPa
        "posicao_virabrequim_ckp": random.randint(0, 360),  # Graus
        "detonacao": random.choice([True, False])  # Booleano
    }
    return data

def calculate_injection(sensor_data):
    """Simula o cálculo do tempo de injeção com base nos dados dos sensores.
    Esta é uma simplificação; em um sistema real, seria um algoritmo complexo.
    """
    # Exemplo simplificado de cálculo de injeção
    injection_time_ms = 5.0  # Valor base em milissegundos

    if sensor_data["sonda_lambda"] < 0.4:  # Mistura pobre
        injection_time_ms *= 1.2
    elif sensor_data["sonda_lambda"] > 0.6:  # Mistura rica
        injection_time_ms *= 0.8

    if sensor_data["temperatura_motor_ect"] < 80.0:  # Motor frio
        injection_time_ms *= 1.1

    if sensor_data["posicao_borboleta_tps"] > 80.0:  # Aceleração total
        injection_time_ms *= 1.5

    # Adicionar lógica para MAP, CKP, etc.

    return round(injection_time_ms, 2)

def send_logs_to_raspberry_pi(log_data):
    """Simula o envio de logs para o Raspberry Pi.
    Em um sistema real, isso seria via UART, SPI, I2C ou MQTT.
    """
    print(f"[ESP32 Log] Enviando para Raspberry Pi: {log_data}")
    # Aqui seria a implementação real da comunicação (e.g., serial.write(str(log_data)))

def main():
    print("Iniciando simulador ESP32 para injeção eletrônica...")
    while True:
        sensor_data = read_sensors()
        injection_time = calculate_injection(sensor_data)

        log_entry = {
            "timestamp": time.time(),
            "sensor_data": sensor_data,
            "injection_time_ms": injection_time,
            "status": "OK"
        }

        send_logs_to_raspberry_pi(log_entry)

        # Simula o ciclo de injeção e espera um curto período
        time.sleep(0.1)  # 100ms para simular um ciclo rápido

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Simulador ESP32 encerrado.")

