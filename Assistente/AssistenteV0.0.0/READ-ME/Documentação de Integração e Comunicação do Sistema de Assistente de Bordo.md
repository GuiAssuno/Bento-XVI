# Documentação de Integração e Comunicação do Sistema de Assistente de Bordo

## 1. Introdução

Este documento detalha os protocolos e métodos de comunicação e integração entre os principais componentes do sistema de assistente de bordo inteligente: o Subsistema de Controle do Motor (ESP32), o Subsistema de Assistente de Bordo (Raspberry Pi 5) e os periféricos do veículo. Uma comunicação eficiente e robusta é crucial para o desempenho e a segurança do sistema.

## 2. Integração entre ESP32 e Raspberry Pi 5

A comunicação entre o ESP32, responsável pelo controle da injeção eletrônica e leitura de sensores do motor, e o Raspberry Pi 5, que atua como a CPU central da assistente de bordo, é um ponto crítico da arquitetura. A escolha do protocolo deve equilibrar velocidade, confiabilidade e complexidade de implementação.

### 2.1. Protocolos de Comunicação

Diversas opções de protocolos podem ser empregadas para a comunicação entre o ESP32 e o Raspberry Pi 5, cada uma com suas vantagens e desvantagens:

| Protocolo           | Vantagens                                                 | Desvantagens                                                | Cenário de Uso Recomendado                                |
| :------------------ | :-------------------------------------------------------- | :---------------------------------------------------------- | :-------------------------------------------------------- |
| **UART/Serial**     | Simples de implementar, baixo overhead, bom para dados contínuos. | Distância limitada, suscetível a ruídos, não ideal para grandes volumes de dados. | Troca de logs e dados de sensores em tempo real, ponto a ponto. |
| **SPI/I2C**         | Alta velocidade, baixa latência, ideal para comunicação entre microcontroladores. | Complexidade de fiação, distância limitada, requer sincronização. | Dados críticos de controle do motor que exigem resposta rápida. |
| **MQTT sobre Wi-Fi** | Flexível, escalável, comunicação sem fio, permite múltiplos clientes e *publish/subscribe*. | Maior latência que serial/SPI, requer um broker MQTT (pode rodar no Raspberry Pi). | Envio de logs de desempenho, telemetria, comandos de alto nível. |

Para este projeto, considerando a necessidade de envio constante de logs e dados de sensores do ESP32 para o Raspberry Pi 5, uma combinação de protocolos pode ser a mais eficaz. Por exemplo, **SPI/I2C** para dados críticos de controle da injeção que exigem baixa latência e **MQTT sobre Wi-Fi** para o envio de logs de desempenho e telemetria, oferecendo flexibilidade e escalabilidade.

### 2.2. Fluxo de Dados

O ESP32 coletará dados dos sensores do motor (sonda lambda, ECT, TPS, MAP, CKP, detonação) e calculará o tempo de injeção. Esses dados, juntamente com o tempo de injeção calculado e um timestamp, serão empacotados como logs. O ESP32 enviará esses logs de forma contínua para o Raspberry Pi 5. O Raspberry Pi 5, por sua vez, receberá e processará esses logs para atualizar a interface do usuário com informações do motor, alimentar o módulo de Machine Learning para análise de padrões e previsão de falhas, e armazenar dados históricos para estatísticas de desempenho e economia.

## 3. Integração entre Raspberry Pi 5 e Periféricos do Veículo

O Raspberry Pi 5 atuará como o hub central para controlar e interagir com diversos periféricos e sistemas do veículo, desde instrumentos analógicos e digitais até câmeras e sistemas de áudio.

### 3.1. Interfaces e Conexões

A integração com os periféricos do veículo será realizada através de uma variedade de interfaces:

| Interface/Conexão | Função Principal                                          | Detalhes de Implementação                                 |
| :---------------- | :-------------------------------------------------------- | :-------------------------------------------------------- |
| **CAN Bus**       | Interação com sistemas eletrônicos existentes do veículo e futuras expansões. | Requer um transceptor CAN Bus (e.g., MCP2515) e uma biblioteca de software para interpretar e enviar mensagens CAN. |
| **GPIO**          | Controle direto de luzes, relés e outros componentes elétricos. | Utilização dos pinos GPIO do Raspberry Pi para acionar relés que controlam cargas maiores (luzes, buzina, etc.). |
| **USB**           | Conexão para câmeras, módulos GPS externos e outros periféricos. | Portas USB 3.0 do Raspberry Pi 5 para câmeras de alta resolução e módulos GPS para maior precisão. |
| **Áudio**         | Saída de áudio para alto-falantes do veículo e entrada para microfone. | Placa de som USB externa ou interface de áudio de alta qualidade para melhor desempenho de voz da assistente e reconhecimento de fala. |
| **Display**       | Exibição de informações visuais (mapas, dados do motor, interface da assistente). | Conexão via HDMI ou DSI para uma tela sensível ao toque no painel do veículo. |

### 3.2. Fluxo de Controle e Dados

O Raspberry Pi 5 receberá comandos de voz do motorista através do microfone, processará esses comandos usando a IA e, com base neles, enviará sinais de controle para os periféricos do veículo. Por exemplo, ao receber um **comando de voz** como "Ligar faróis", a **IA processará** e identificará a intenção, levando o Raspberry Pi a enviar um sinal via GPIO para um relé que aciona os faróis.

Da mesma forma, dados de câmeras serão processados pelo módulo de Visão Computacional da IA para detecção de semáforos, reconhecimento de veículos e monitoramento de pontos cegos, fornecendo feedback visual ou sonoro ao motorista.

## 4. Considerações de Segurança e Robustez

A integração de sistemas em um ambiente automotivo exige atenção especial à segurança e robustez. Isso inclui o **isolamento elétrico** para proteger os componentes contra picos de tensão e ruídos, um **gerenciamento de energia** confiável para garantir o desligamento seguro e a inicialização rápida do Raspberry Pi, o desenvolvimento de **lógicas de *fail-safe*** para funções críticas (como a injeção eletrônica) e a implementação de **atualizações Over-the-Air (OTA)** para o software do ESP32 e Raspberry Pi de forma segura e eficiente.

## 5. Próximos Passos

Os próximos passos envolvem a seleção de hardware específico para as interfaces (transceptores CAN, módulos de áudio, câmeras), o desenvolvimento de drivers e bibliotecas de software para cada interface, e a implementação dos protocolos de comunicação escolhidos. Testes rigorosos de comunicação e integração serão essenciais para validar a robustez e o desempenho do sistema.
