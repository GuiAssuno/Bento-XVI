# Arquitetura do Sistema de Assistente de Bordo Inteligente para Chevrolet Opala Comodoro 4.1 (1982)

## 1. Introdução

Este documento detalha a arquitetura proposta para um sistema de assistente de bordo inteligente, projetado para modernizar um Chevrolet Opala Comodoro 4.1, ano 1982. O objetivo é integrar tecnologias avançadas para auxiliar o motorista na tomada de decisões, monitoramento personalizado, e redução de acidentes, focando em segurança, eficiência e uma experiência de condução aprimorada. O sistema abordará a conversão do motor carburado para injeção eletrônica controlada por ESP32 e a implementação de uma assistente virtual com inteligência artificial rodando em um Raspberry Pi 5.

## 2. Visão Geral do Sistema

O sistema será composto por dois subsistemas principais interconectados: o **Subsistema de Controle do Motor (ESP32)**, responsável pela gestão da injeção eletrônica, coleta de dados de sensores do motor e comunicação com a CPU central; e o **Subsistema de Assistente de Bordo (Raspberry Pi 5)**, que atuará como a CPU central, gerenciando a interface com o usuário (voz, tela), processando dados, executando a IA e controlando diversas funcionalidades do veículo.

## 3. Componentes Principais e Suas Funções

### 3.1. Chevrolet Opala Comodoro 4.1 (1982)

O veículo base para este projeto é um **Chevrolet Opala Comodoro 4.1, ano 1982**, equipado com um motor de 4.1 litros e 4 cilindros, originalmente carburado. O principal desafio é modernizar o sistema de alimentação de combustível para injeção eletrônica, mantendo a integridade e o caráter do veículo clássico.

### 3.2. Subsistema de Controle do Motor (ESP32)

O **Subsistema de Controle do Motor** será baseado em uma placa **ESP32** (ou variantes como ESP32-S3/C3/WROOM, a escolha dependerá dos requisitos específicos de processamento e conectividade). As funções primárias deste subsistema incluem a **leitura de sensores** para monitorar parâmetros críticos do motor, como oxigênio (sonda lambda), temperatura do motor (ECT), temperatura do ar de admissão (IAT), pressão do coletor (MAP), posição do virabrequim (CKP), posição da borboleta (TPS) e nível de óleo. Além disso, será responsável pelo **controle da injeção eletrônica**, realizando o cálculo e ajuste preciso do tempo de injeção de combustível e do ponto de ignição, substituindo o sistema de carburador original.

A **otimização de processamento** é crucial, com prioridade máxima na velocidade para evitar falhas que possam comprometer a eficiência do motor. O ESP32 também será encarregado da **geração de logs**, enviando constantemente dados de desempenho do motor para a CPU central (Raspberry Pi 5) para monitoramento e análise em tempo real.

Os **sensores essenciais** para este subsistema incluem:

| Sensor                   | Função Principal                                          |
| :----------------------- | :-------------------------------------------------------- |
| Sonda Lambda (Oxigênio)  | Monitoramento da mistura ar/combustível                   |
| Temperatura do Motor (ECT) | Ajuste da injeção em diferentes temperaturas              |
| Posição da Borboleta (TPS) | Identificação da demanda de potência do motor             |
| Pressão Absoluta do Coletor (MAP) | Medição da carga do motor                                 |
| Posição do Virabrequim (CKP) | Sincronismo da injeção e ignição                          |
| Detonação                | Ajuste do ponto de ignição e proteção do motor            |


### 3.3. Subsistema de Assistente de Bordo (Raspberry Pi 5 16GB)

O **Subsistema de Assistente de Bordo** terá como **CPU Central** um **Raspberry Pi 5 com 16GB de RAM**. Suas **funções** abrangem o **processamento de dados** recebidos do ESP32 e de outros sensores do veículo, servindo como o cérebro do sistema.

A **Assistente Virtual com IA** será um componente central, oferecendo **comandos de voz e respostas** para uma interação intuitiva com o motorista. Ela possuirá um **conhecimento geral e avançado em mecânica**, sendo capaz de responder a dúvidas sobre motores e veículos, reconhecer outros modelos de carros, e prever potenciais falhas. A **visão computacional** permitirá a detecção de semáforos, reconhecimento de outros veículos e monitoramento de pontos cegos. Através de **Machine Learning**, a assistente se adaptará, aprenderá continuamente e personalizará as preferências do usuário. Uma característica crucial é o **funcionamento offline**, garantindo a operação mesmo em áreas sem conexão à internet.

Outras funcionalidades incluem o **controle de instrumentos** do veículo, como luzes, sistema de som e integração com plataformas como Spotify. Para **navegação e localização**, o sistema oferecerá GPS preciso, informações de trânsito em tempo real, sugestão de rotas mais rápidas e previsão de engarrafamentos. O **monitoramento de desempenho** incluirá estatísticas de economia de combustível, dados de viagem e telemetria do veículo. Em termos de **segurança ativa**, a assistente poderá prever acidentes, emitir alertas de pontos cegos e auxiliar na direção. O **gerenciamento de câmeras** permitirá o controle de múltiplas câmeras (internas/externas) para monitoramento e gravação, e a **criação de rotas** otimizadas. Futuramente, a assistente poderá evoluir para um **copiloto** com funções de **piloto automático**.
Os **periféricos e integrações** necessários para o Raspberry Pi 5 são:

| Periférico/Integração | Função                                                    |
| :-------------------- | :-------------------------------------------------------- |
| Microfone e Alto-falantes | Interação por voz com a assistente                        |
| Tela (Display)        | Exibição de informações visuais (mapas, dados do motor)   |
| Módulos de Comunicação | Wi-Fi, Bluetooth, GPS para conectividade e localização    |
| Interface CAN Bus     | Comunicação com sistemas eletrônicos do veículo           |
| Câmeras               | Múltiplas câmeras para visão computacional e monitoramento|


## 4. Comunicação e Integração

### 4.1. ESP32 e Raspberry Pi 5

A **comunicação entre o ESP32 e o Raspberry Pi 5** deve ser rápida e confiável. As opções de protocolo incluem:

| Protocolo           | Característica Principal                                  |
| :------------------ | :-------------------------------------------------------- |
| UART/Serial         | Simples e direto para troca de dados em tempo real         |
| SPI/I2C             | Comunicação de alta velocidade e baixa latência           |
| MQTT sobre Wi-Fi    | Flexível e escalável, permitindo comunicação sem fio e integração com outros dispositivos (requer broker MQTT, que pode rodar no Raspberry Pi) |

O **fluxo de dados** prevê que o ESP32 enviará logs e dados de sensores de forma contínua para o Raspberry Pi 5, que os processará e utilizará para a IA e exibição ao motorista.

### 4.2. Raspberry Pi 5 e Periféricos do Veículo

A integração do Raspberry Pi 5 com os periféricos do veículo será realizada através de:

| Interface/Conexão | Função                                                    |
| :---------------- | :-------------------------------------------------------- |
| CAN Bus           | Interação com sistemas eletrônicos existentes e expansões |
| GPIO              | Controle direto de luzes, relés e componentes elétricos   |
| USB               | Conexão para câmeras, módulos GPS externos e periféricos  |
| Áudio             | Saída de áudio para alto-falantes do veículo e entrada para microfone |


## 5. Considerações de Segurança e Desempenho

As **considerações de segurança e desempenho** são fundamentais para o sucesso deste projeto. É imperativo implementar mecanismos de **redundância e tolerância a falhas** para garantir que eventuais problemas em um subsistema não comprometam a segurança ou a funcionalidade crítica do veículo. A **velocidade de processamento** deve ser otimizada no ESP32 para assegurar tempos de resposta mínimos no controle da injeção, enquanto o Raspberry Pi 5 deve possuir recursos suficientes para lidar com a IA e multitarefas de forma eficiente. A **confiabilidade** será garantida pela utilização de componentes de grau automotivo (sempre que possível) e por testes rigorosos em todas as etapas do desenvolvimento. O sistema deve ter uma **inicialização rápida**, ligando junto com o carro, sem a necessidade de intervenção do motorista. Por fim, o **ambiente de risco** automotivo (vibração, temperatura, variações de energia) deve ser cuidadosamente considerado no design para garantir a robustez do hardware e software.

## 6. Próximos Passos

Os **próximos passos** para a implementação deste projeto incluem:

| Etapa                                  | Descrição                                                                   |
| :------------------------------------- | :-------------------------------------------------------------------------- |
| **Seleção Detalhada de Sensores e Atuadores** | Definir modelos específicos e fornecedores para todos os componentes.       |
| **Desenvolvimento do Firmware do ESP32**      | Programação da lógica de controle da injeção e comunicação com o Raspberry Pi. |
| **Desenvolvimento do Software da Assistente de Bordo** | Implementação da IA, interface de voz e integração com periféricos do veículo. |
| **Testes e Calibração**                | Realização de testes extensivos em bancada e no veículo para garantir funcionalidade e segurança. |


## Referências

[1] To wear a suit! Diplomat 4.1 from carbureted to injected! (2022). YouTube. Disponível em: [https://www.youtube.com/watch?v=R5o5MxaI0bA](https://www.youtube.com/watch?v=R5o5MxaI0bA)
[2] INJEÇÃO ELETRÔNICA EM MOTOR ANTIGO (2024). YouTube. Disponível em: [https://www.youtube.com/watch?v=0SYGucdRQlo](https://www.youtube.com/watch?v=0SYGucdRQlo)
[3] Guia de Como Transformar um Carro Carburado em Injetado. Canal da Peça. Disponível em: [https://www.canaldapeca.com.br/blog/como-transformar-um-carro-carburado-em-injetado/](https://www.canaldapeca.com.br/blog/como-transformar-um-carro-carburado-em-injetado/)
[4] MOTOR DE OPALA COM INJEÇÃO DO OMEGA 4.1 (2013). Opaleiros do Paraná. Disponível em: [https://opaleirosdoparana.forumeiros.com/t30187-motor-de-opala-com-injecao-do-omega-4-1](https://opaleirosdoparana.forumeiros.com/t30187-motor-de-opala-com-injecao-do-omega-4-1) 
