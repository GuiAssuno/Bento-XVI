# Assistente de Bordo Inteligente para Chevrolet Opala Comodoro 4.1 (1982)

Este projeto visa modernizar um Chevrolet Opala Comodoro 4.1 de 1982, integrando um sistema de assistente de bordo inteligente. O sistema é composto por um backend em Python (Flask) rodando em um Raspberry Pi 5 e um frontend em HTML/CSS/JavaScript, além de simular o controle de injeção eletrônica via ESP32.

## Estrutura do Projeto

```
assistente_bordo_opala/
├── backend/                          # Código do servidor Flask e módulos da assistente
│   ├── api/                          # Módulos para definir rotas da API (opcional, para maior modularidade)
│   ├── data/                         # Armazenamento de dados (logs, preferências, etc.)
│   ├── modules/                      # Módulos principais da assistente (voz, veículo, ML, etc.)
│   │   ├── __init__.py
│   │   ├── voice_interface.py
│   │   ├── vehicle_control.py
│   │   ├── knowledge_base.py
│   │   ├── computer_vision.py
│   │   ├── machine_learning.py
│   │   ├── data_processor.py
│   │   └── esp32_injection_simulator.py # Simulação do ESP32
│   ├── app.py                        # Aplicação Flask principal
│   └── requirements.txt              # Dependências do Python
├── frontend/                         # Código do frontend (interface do usuário)
│   ├── static/                       # Arquivos estáticos (CSS, JS, imagens)
│   │   ├── css/
│   │   ├── js/
│   │   │   └── app.js                # Lógica JavaScript do frontend
│   │   └── assets/                   # Imagens, ícones, etc.
│   └── templates/                    # Templates HTML (servidos pelo Flask)
│       └── index.html                # Interface principal
├── docs/                             # Documentação adicional do projeto
├── tests/                            # Testes automatizados
└── start.sh                          # Script para iniciar o backend
```

## Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter o Python 3.11 (ou superior) e `pip` instalados.

### 1. Configuração do Backend

1.  **Navegue até o diretório do backend:**
    ```bash
    cd assistente_bordo_opala/backend
    ```

2.  **Instale as dependências do Python:**
    ```bash
    pip install -r requirements.txt
    ```
    *Se encontrar problemas de permissão, tente `sudo pip install -r requirements.txt`.*

### 2. Iniciar o Backend

Após instalar as dependências, você pode iniciar o servidor Flask a partir do diretório raiz do projeto:

```bash
cd assistente_bordo_opala
./start.sh
```

O servidor será iniciado em `http://127.0.0.1:5000`. Você verá mensagens de inicialização dos módulos da assistente e do Flask no terminal.

### 3. Acessar o Frontend

Com o backend rodando, abra seu navegador web e acesse:

```
http://127.0.0.1:5000/
```

Você verá a interface da assistente de bordo. O frontend se comunicará com o backend através das APIs REST para obter dados do motor, enviar comandos, etc.

### Funcionalidades Básicas Implementadas (Simuladas)

*   **Menu Interativo:** Clique no ícone de "home" no canto superior direito para abrir/fechar o menu de funcionalidades. Você também pode pressionar a tecla `M` para simular um comando de voz "mostrar menu".
*   **Comandos de Texto:** Use a caixa de texto na parte inferior da tela para enviar comandos ao backend (ex: "Qual a temperatura do motor?", "Ligar faróis", "Tocar Spotify", "O que é um carburador?").
*   **Monitoramento do Motor:** Os anéis de dados (Temperatura, RPM, Combustível) são atualizados com dados simulados do ESP32 via backend.
*   **Controle de Luzes:** Envie o comando "Ligar faróis" ou "Desligar faróis" via texto.
*   **Controle de Música:** Envie o comando "Tocar Spotify" ou "Parar música" via texto.
*   **Base de Conhecimento:** Pergunte sobre "carburador" ou "injeção eletrônica".
*   **Visão Computacional:** Os dados de câmera são simulados e podem ser acessados via API, embora não sejam exibidos diretamente no frontend ainda.

## Próximos Passos

*   Implementar a lógica real de comunicação com ESP32 e sensores físicos.
*   Desenvolver a interface visual para as funcionalidades de navegação, câmera e estatísticas de desempenho.
*   Expandir a base de conhecimento e a capacidade de processamento de linguagem natural da IA.
*   Implementar o módulo de visão computacional para processamento de vídeo em tempo real.
*   Adicionar autenticação e segurança para as APIs.
*   Otimizar o desempenho para o ambiente embarcado do Raspberry Pi.

---
