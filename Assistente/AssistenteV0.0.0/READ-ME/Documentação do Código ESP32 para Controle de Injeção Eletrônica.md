# Documentação do Código ESP32 para Controle de Injeção Eletrônica

## 1. Introdução

Este documento descreve o código simulado para o subsistema de controle do motor baseado no ESP32, responsável pela gestão da injeção eletrônica e coleta de dados de sensores. O objetivo é demonstrar a lógica de leitura de sensores, cálculo do tempo de injeção e envio de logs para a CPU central (Raspberry Pi 5).

## 2. Visão Geral do Código

O código `esp32_injection_simulator.py` simula as principais funções que seriam executadas por um ESP32 em um sistema de injeção eletrônica. Ele inclui:

*   **`read_sensors()`:** Simula a leitura de dados de diversos sensores do motor.
*   **`calculate_injection()`:** Simula o cálculo do tempo de injeção com base nos dados dos sensores.
*   **`send_logs_to_raspberry_pi()`:** Simula o envio dos dados processados e logs para o Raspberry Pi 5.
*   **`main()`:** A função principal que orquestra a leitura, cálculo e envio em um loop contínuo.

## 3. Detalhes da Implementação

### 3.1. `read_sensors()`

Esta função gera valores aleatórios para simular as leituras dos sensores do motor. Em um ambiente real, esta função seria responsável por interagir com os pinos GPIO do ESP32 e ler os valores analógicos/digitais dos sensores físicos.

```python
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
```

### 3.2. `calculate_injection()`

Esta função simula a lógica de cálculo do tempo de injeção. Em um sistema real, este seria um algoritmo complexo que levaria em consideração mapas de injeção (fuel maps), correção por temperatura, carga do motor, feedback da sonda lambda, entre outros fatores. A simulação atual demonstra um ajuste básico baseado na sonda lambda, temperatura do motor e posição da borboleta.

```python
def calculate_injection(sensor_data):
    """Simula o cálculo do tempo de injeção com base nos dados dos sensores.
    Esta é uma simplificação; em um sistema real, seria um algoritmo complexo.
    """
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
```

### 3.3. `send_logs_to_raspberry_pi()`

Esta função simula o envio de dados para o Raspberry Pi. Em uma implementação real, a comunicação seria estabelecida através de protocolos como UART, SPI, I2C ou MQTT sobre Wi-Fi, conforme detalhado na documentação de arquitetura. O `log_data` conteria todas as informações relevantes dos sensores e o tempo de injeção calculado.

```python
def send_logs_to_raspberry_pi(log_data):
    """Simula o envio de logs para o Raspberry Pi.
    Em um sistema real, isso seria via UART, SPI, I2C ou MQTT.
    """
    print(f"[ESP32 Log] Enviando para Raspberry Pi: {log_data}")
    # Aqui seria a implementação real da comunicação (e.g., serial.write(str(log_data)))
```

### 3.4. `main()`

A função `main` executa um loop infinito onde os sensores são lidos, o tempo de injeção é calculado e os logs são enviados. Um `time.sleep(0.1)` simula o intervalo entre os ciclos de injeção, garantindo que a simulação não consuma 100% da CPU e represente um comportamento mais realista de um microcontrolador.

```python
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

        time.sleep(0.1)  # 100ms para simular um ciclo rápido
```

## 4. Considerações para Implementação Real

*   **Hardware:** A escolha exata do modelo ESP32 (e.g., ESP32-WROOM, ESP32-S3) dependerá dos requisitos de pinos GPIO, memória e poder de processamento para o algoritmo de injeção e comunicação.
*   **Sensores:** A calibração e a precisão dos sensores são cruciais para o funcionamento correto da injeção eletrônica.
*   **Atuadores:** O ESP32 precisaria controlar os injetores de combustível e o sistema de ignição através de drivers de potência adequados.
*   **Algoritmo de Injeção:** O `calculate_injection` real seria muito mais complexo, envolvendo tabelas 3D (mapas de combustível e ignição) e correções dinâmicas.
*   **Comunicação:** A comunicação com o Raspberry Pi deve ser robusta e com tratamento de erros para garantir a integridade dos dados.
*   **Segurança:** Falhas no sistema de injeção podem ser críticas. Mecanismos de *fail-safe* e redundância devem ser considerados.

## 5. Próximos Passos

O próximo passo seria refinar o algoritmo de injeção, integrar drivers de hardware para injetores e ignição, e estabelecer a comunicação real com o Raspberry Pi utilizando um dos protocolos definidos na arquitetura geral do sistema.
