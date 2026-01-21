# Arquitetura de Sistema Crítico - Assistente de Bordo Opala 1982

## Visão Geral

Este documento descreve a arquitetura otimizada para o sistema de assistente de bordo automotivo, projetado para operar em ambiente crítico com requisitos rigorosos de performance, confiabilidade e tempo real.

## Stack Tecnológica Recomendada

### Frontend (Interface Visual)
- **React 18+** com modo concorrente para renderização não-bloqueante
- **Electron** para aplicação desktop nativa na Raspberry Pi 5
- **WebGL/Canvas** para visualizações de alta performance
- **Web Workers** para processamento paralelo sem bloquear UI

### Backend/Middleware (Raspberry Pi 5)
- **Node.js com C++ Addons** para operações críticas de baixo nível
- **WebSocket/Socket.io** para comunicação em tempo real com ESP32
- **MQTT** para mensageria leve e confiável entre dispositivos
- **Redis** para cache de dados de sensores em memória

### Hardware Interface
- **ESP32** via Serial/UART ou WiFi/MQTT
- **Geolocation API** ou GPS via Serial (NMEA)
- **V4L2** para câmeras (Video4Linux2)
- **ALSA/PulseAudio** para áudio

## Otimizações Implementadas

### 1. Componentes React Otimizados

#### React.memo
Todos os componentes foram envolvidos em `React.memo` para evitar re-renders desnecessários quando as props não mudam.

```javascript
const LoadingRing = React.memo(({ value, max, size, strokeWidth }) => {
  // Componente só re-renderiza se value, max, size ou strokeWidth mudarem
});
```

#### useMemo
Cálculos pesados são memoizados para evitar recálculos em cada render.

```javascript
const { radius, circumference, offset, strokeColor } = useMemo(() => {
  // Cálculos complexos executados apenas quando dependências mudam
}, [value, max, size, strokeWidth]);
```

#### useCallback
Funções são memoizadas para evitar recriação em cada render.

```javascript
const draw = useCallback(() => {
  // Função de desenho memoizada
}, [isTransmittingSound, frequencies]);
```

### 2. Canvas e Animações

#### requestAnimationFrame
Todas as animações usam `requestAnimationFrame` para sincronização com taxa de atualização do display (60 FPS).

```javascript
const animate = () => {
  draw();
  animationFrameRef.current = requestAnimationFrame(animate);
};
```

#### Canvas Context Options
Canvas configurado com `alpha: false` para melhor performance quando transparência não é necessária.

```javascript
const ctx = canvas.getContext('2d', { alpha: false });
```

#### GPU Acceleration
Propriedade `willChange` usada para indicar ao navegador quais propriedades serão animadas, permitindo otimização de GPU.

```javascript
style={{ willChange: 'transform' }}
```

### 3. Gerenciamento de Memória

#### Cleanup de Efeitos
Todos os `useEffect` têm funções de cleanup para evitar memory leaks.

```javascript
useEffect(() => {
  const interval = setInterval(() => { /* ... */ }, 1000);
  return () => clearInterval(interval); // Cleanup
}, []);
```

#### Refs para Intervalos
Uso de `useRef` para armazenar referências de intervalos e animações.

```javascript
const animationFrameRef = useRef(null);
// ...
return () => {
  if (animationFrameRef.current) {
    cancelAnimationFrame(animationFrameRef.current);
  }
};
```

## Integração com Hardware

### Comunicação ESP32 → Raspberry Pi

#### Opção 1: Serial/UART (Recomendado para Dados Críticos)
- **Vantagens:** Baixa latência, confiável, sem overhead de rede
- **Implementação:** Node.js com `serialport` package
- **Taxa de Baud:** 115200 ou superior

```javascript
// Exemplo de integração (Node.js backend)
const SerialPort = require('serialport');
const port = new SerialPort('/dev/ttyUSB0', { baudRate: 115200 });

port.on('data', (data) => {
  // Parse dados dos sensores
  const sensorData = JSON.parse(data.toString());
  // Enviar para frontend via WebSocket
  io.emit('sensor-data', sensorData);
});
```

#### Opção 2: MQTT (Recomendado para Múltiplos Dispositivos)
- **Vantagens:** Pub/Sub, QoS configurável, leve
- **Broker:** Mosquitto na Raspberry Pi
- **Implementação:** `mqtt.js` no frontend/backend

```javascript
// Exemplo de integração (Frontend)
import mqtt from 'mqtt';

const client = mqtt.connect('mqtt://localhost:1883');

client.on('connect', () => {
  client.subscribe('sensors/engine/#');
});

client.on('message', (topic, message) => {
  const data = JSON.parse(message.toString());
  // Atualizar estado React
  setSensorData(data);
});
```

### Dados de Sensores em Tempo Real

#### Estrutura de Dados Recomendada (JSON)
```json
{
  "timestamp": 1634567890123,
  "engine": {
    "rpm": 3500,
    "temperature": 85,
    "oil_pressure": 45,
    "oxygen": 14.7
  },
  "fuel": {
    "injection_time": 12.5,
    "consumption": 8.5
  },
  "sensors": {
    "ultrasonic_front": 150,
    "ultrasonic_rear": 200
  }
}
```

#### Atualização de Estado Eficiente
Use `useReducer` para gerenciar estado complexo de sensores.

```javascript
const sensorReducer = (state, action) => {
  switch (action.type) {
    case 'UPDATE_ENGINE':
      return { ...state, engine: action.payload };
    case 'UPDATE_FUEL':
      return { ...state, fuel: action.payload };
    default:
      return state;
  }
};

const [sensorData, dispatch] = useReducer(sensorReducer, initialState);
```

### Câmeras (Pontos Cegos)

#### V4L2 (Video4Linux2)
- **Implementação:** FFmpeg para streaming de vídeo
- **Protocolo:** RTSP ou WebRTC para baixa latência
- **Resolução:** 640x480 ou 1280x720 (balancear qualidade vs. performance)

```bash
# Exemplo de streaming com FFmpeg
ffmpeg -f v4l2 -i /dev/video0 -vcodec libx264 -preset ultrafast -tune zerolatency -f rtsp rtsp://localhost:8554/camera1
```

### GPS

#### NMEA via Serial
```javascript
const GPS = require('gps');
const gps = new GPS();

port.on('data', (data) => {
  gps.update(data.toString());
  if (gps.state.lat && gps.state.lon) {
    setLatitude(gps.state.lat);
    setLongitude(gps.state.lon);
  }
});
```

## Performance Crítica

### Benchmarks Alvo (Raspberry Pi 5)
- **Latência de Atualização de Sensores:** < 50ms
- **Frame Rate da Interface:** 60 FPS constante
- **Uso de CPU:** < 30% em operação normal
- **Uso de RAM:** < 500 MB
- **Tempo de Boot:** < 5 segundos

### Otimizações de Sistema Operacional

#### 1. Usar Raspberry Pi OS Lite (sem Desktop)
Reduz overhead do sistema operacional.

#### 2. Configurar Electron em Modo Kiosk
```javascript
// main.js do Electron
const mainWindow = new BrowserWindow({
  fullscreen: true,
  kiosk: true,
  frame: false,
  webPreferences: {
    nodeIntegration: true,
    contextIsolation: false,
    hardwareAcceleration: true, // Importante!
  }
});
```

#### 3. Prioridade de Processo
```bash
# Executar com prioridade alta
nice -n -10 npm start
```

#### 4. Overclocking (Opcional, com Cuidado)
```bash
# /boot/config.txt
arm_freq=2400
gpu_freq=750
over_voltage=6
```

## Confiabilidade e Segurança

### 1. Watchdog Timer
Implementar watchdog para reiniciar aplicação em caso de travamento.

```javascript
// Node.js
const watchdog = require('watchdog');
watchdog.start(5000); // 5 segundos

setInterval(() => {
  watchdog.reset(); // Reset watchdog se aplicação está rodando
}, 1000);
```

### 2. Logging e Monitoramento
```javascript
// Winston para logging estruturado
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

### 3. Fallback e Redundância
- **Dados de Sensores:** Implementar valores padrão seguros em caso de falha
- **GPS:** Usar última posição conhecida se sinal for perdido
- **Câmeras:** Mostrar placeholder se stream falhar

## Próximos Passos

1. **Implementar Backend Node.js** para comunicação com ESP32
2. **Configurar MQTT Broker** na Raspberry Pi
3. **Integrar Web Audio API** para análise de frequência real
4. **Implementar Geolocation API** ou GPS via Serial
5. **Configurar FFmpeg** para streaming de câmeras
6. **Empacotar com Electron** para deploy na Raspberry Pi
7. **Testes de Stress** e otimização de performance
8. **Implementar Watchdog** e sistema de recuperação de falhas

## Considerações de Segurança Automotiva

- **ISO 26262 (ASIL):** Para sistemas críticos de segurança, considerar certificação
- **Testes de Vibração:** Interface deve ser robusta a vibrações do veículo
- **Temperatura:** Raspberry Pi deve ter dissipação adequada (cooler ativo)
- **Alimentação:** UPS ou bateria backup para evitar desligamento abrupto
- **CAN Bus:** Para integração futura com sistemas do veículo (OBD-II)

## Conclusão

Esta arquitetura foi projetada para máxima performance, confiabilidade e eficiência em ambiente automotivo crítico. Todas as otimizações implementadas visam garantir operação em tempo real com mínimo overhead e máxima responsividade.

