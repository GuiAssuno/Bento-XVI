# Guia de Implementação - Sistema Crítico Automotivo

## Passo a Passo para Deploy na Raspberry Pi 5

### 1. Preparação do Sistema Operacional

#### Instalar Raspberry Pi OS Lite (64-bit)
```bash
# Baixar Raspberry Pi Imager
# Selecionar: Raspberry Pi OS Lite (64-bit)
# Configurar SSH e WiFi durante instalação
```

#### Atualizar Sistema
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl build-essential
```

#### Instalar Node.js 20 LTS
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node --version  # Verificar instalação
```

### 2. Configuração do Projeto

#### Clonar/Copiar Projeto
```bash
cd /home/pi
# Copiar projeto via SCP ou git clone
```

#### Instalar Dependências
```bash
cd 80s-wave-interface-optimized
npm install
```

#### Instalar Electron
```bash
npm install --save-dev electron electron-builder
```

### 3. Configurar Electron para Kiosk Mode

#### Criar main.js
```javascript
// main.js
const { app, BrowserWindow } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    fullscreen: true,
    kiosk: true,
    frame: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
      hardwareAcceleration: true,
    }
  });

  // Carregar aplicação
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
  } else {
    mainWindow.loadFile(path.join(__dirname, 'dist', 'index.html'));
  }

  // Desabilitar menu
  mainWindow.setMenu(null);

  // DevTools (apenas desenvolvimento)
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
```

#### Atualizar package.json
```json
{
  "name": "assistente-bordo-opala",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "electron": "electron .",
    "electron:dev": "NODE_ENV=development electron .",
    "electron:build": "npm run build && electron-builder"
  },
  "build": {
    "appId": "com.opala.assistente",
    "productName": "Assistente Opala",
    "linux": {
      "target": "dir",
      "category": "Utility"
    }
  }
}
```

### 4. Integração com ESP32

#### Instalar SerialPort
```bash
npm install serialport
```

#### Criar backend/server.js
```javascript
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { SerialPort } = require('serialport');
const { ReadlineParser } = require('@serialport/parser-readline');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Configurar porta serial
const port = new SerialPort({
  path: '/dev/ttyUSB0',
  baudRate: 115200
});

const parser = port.pipe(new ReadlineParser({ delimiter: '\n' }));

// Receber dados do ESP32
parser.on('data', (data) => {
  try {
    const sensorData = JSON.parse(data);
    console.log('Dados recebidos:', sensorData);
    
    // Enviar para frontend via WebSocket
    io.emit('sensor-data', sensorData);
  } catch (error) {
    console.error('Erro ao parsear dados:', error);
  }
});

// WebSocket connection
io.on('connection', (socket) => {
  console.log('Cliente conectado');
  
  socket.on('disconnect', () => {
    console.log('Cliente desconectado');
  });
});

server.listen(3000, () => {
  console.log('Servidor rodando na porta 3000');
});
```

#### Integrar WebSocket no Frontend (App.jsx)
```javascript
import { useEffect } from 'react';
import io from 'socket.io-client';

function App() {
  useEffect(() => {
    const socket = io('http://localhost:3000');
    
    socket.on('sensor-data', (data) => {
      // Atualizar estado com dados reais dos sensores
      setLoadValue1(data.engine.rpm / 10); // Exemplo: RPM / 10
      setLoadValue2(data.engine.temperature);
      setLoadValue3(data.fuel.consumption * 10);
    });
    
    return () => socket.disconnect();
  }, []);
  
  // ... resto do código
}
```

### 5. Configurar MQTT (Alternativa ao Serial)

#### Instalar Mosquitto
```bash
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

#### Instalar MQTT.js
```bash
npm install mqtt
```

#### Integrar MQTT no Frontend
```javascript
import mqtt from 'mqtt';

function App() {
  useEffect(() => {
    const client = mqtt.connect('mqtt://localhost:1883');
    
    client.on('connect', () => {
      console.log('Conectado ao MQTT');
      client.subscribe('opala/sensors/#');
    });
    
    client.on('message', (topic, message) => {
      const data = JSON.parse(message.toString());
      
      if (topic === 'opala/sensors/engine') {
        setLoadValue1(data.rpm / 10);
        setLoadValue2(data.temperature);
      }
      
      if (topic === 'opala/sensors/fuel') {
        setLoadValue3(data.consumption * 10);
      }
    });
    
    return () => client.end();
  }, []);
}
```

### 6. Integração com GPS

#### Via Geolocation API (se disponível)
```javascript
useEffect(() => {
  if (navigator.geolocation) {
    const watchId = navigator.geolocation.watchPosition(
      (position) => {
        setLatitude(position.coords.latitude);
        setLongitude(position.coords.longitude);
      },
      (error) => console.error('Erro GPS:', error),
      {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
      }
    );
    
    return () => navigator.geolocation.clearWatch(watchId);
  }
}, []);
```

#### Via Serial (NMEA)
```bash
npm install gps
```

```javascript
// backend/server.js
const GPS = require('gps');
const gps = new GPS();

const gpsPort = new SerialPort({
  path: '/dev/ttyAMA0', // Porta serial do GPS
  baudRate: 9600
});

const gpsParser = gpsPort.pipe(new ReadlineParser({ delimiter: '\r\n' }));

gpsParser.on('data', (data) => {
  gps.update(data);
  
  if (gps.state.lat && gps.state.lon) {
    io.emit('gps-data', {
      latitude: gps.state.lat,
      longitude: gps.state.lon,
      speed: gps.state.speed,
      altitude: gps.state.alt
    });
  }
});
```

### 7. Integração com Câmeras

#### Instalar FFmpeg
```bash
sudo apt install -y ffmpeg
```

#### Streaming de Câmera USB
```bash
# Iniciar stream RTSP
ffmpeg -f v4l2 -i /dev/video0 \
  -vcodec libx264 -preset ultrafast -tune zerolatency \
  -f rtsp rtsp://localhost:8554/camera1
```

#### Atualizar VideoPlayer.jsx
```javascript
const VideoPlayer = React.memo(({ isTransmitting }) => {
  const videoSource = 'rtsp://localhost:8554/camera1';
  
  // ... resto do código
});
```

### 8. Web Audio API para Frequências Reais

```javascript
// hooks/useAudioAnalyzer.js
import { useEffect, useState } from 'react';

export function useAudioAnalyzer() {
  const [frequencies, setFrequencies] = useState([]);
  
  useEffect(() => {
    let audioContext;
    let analyser;
    let dataArray;
    let animationId;
    
    async function setupAudio() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioContext = new AudioContext();
        analyser = audioContext.createAnalyser();
        const source = audioContext.createMediaStreamSource(stream);
        
        source.connect(analyser);
        analyser.fftSize = 128;
        
        const bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);
        
        function updateFrequencies() {
          analyser.getByteFrequencyData(dataArray);
          const normalized = Array.from(dataArray).map(v => v / 255);
          setFrequencies(normalized);
          animationId = requestAnimationFrame(updateFrequencies);
        }
        
        updateFrequencies();
      } catch (error) {
        console.error('Erro ao acessar áudio:', error);
      }
    }
    
    setupAudio();
    
    return () => {
      if (animationId) cancelAnimationFrame(animationId);
      if (audioContext) audioContext.close();
    };
  }, []);
  
  return frequencies;
}
```

### 9. Auto-Start na Inicialização

#### Criar serviço systemd
```bash
sudo nano /etc/systemd/system/assistente-opala.service
```

```ini
[Unit]
Description=Assistente de Bordo Opala
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/80s-wave-interface-optimized
Environment="DISPLAY=:0"
Environment="NODE_ENV=production"
ExecStart=/usr/bin/npm run electron
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Habilitar serviço
```bash
sudo systemctl daemon-reload
sudo systemctl enable assistente-opala
sudo systemctl start assistente-opala
```

### 10. Otimizações de Performance

#### Configurar GPU Memory Split
```bash
sudo nano /boot/config.txt
```

```ini
# Alocar mais memória para GPU
gpu_mem=256

# Overclocking (opcional, testar estabilidade)
arm_freq=2400
gpu_freq=750
over_voltage=6

# Desabilitar Bluetooth se não usado
dtoverlay=disable-bt
```

#### Desabilitar Serviços Desnecessários
```bash
sudo systemctl disable bluetooth
sudo systemctl disable avahi-daemon
sudo systemctl disable triggerhappy
```

### 11. Monitoramento e Logs

#### Instalar PM2 (Process Manager)
```bash
npm install -g pm2
```

#### Configurar PM2
```bash
pm2 start npm --name "assistente-opala" -- run electron
pm2 save
pm2 startup
```

#### Ver logs
```bash
pm2 logs assistente-opala
```

### 12. Backup e Recuperação

#### Criar script de backup
```bash
#!/bin/bash
# backup.sh
tar -czf /home/pi/backup-$(date +%Y%m%d).tar.gz \
  /home/pi/80s-wave-interface-optimized \
  /etc/systemd/system/assistente-opala.service
```

## Testes de Performance

### Benchmark de FPS
```javascript
// Adicionar ao App.jsx
let frameCount = 0;
let lastTime = performance.now();

function measureFPS() {
  frameCount++;
  const currentTime = performance.now();
  
  if (currentTime - lastTime >= 1000) {
    console.log(`FPS: ${frameCount}`);
    frameCount = 0;
    lastTime = currentTime;
  }
  
  requestAnimationFrame(measureFPS);
}

measureFPS();
```

### Monitorar Uso de Recursos
```bash
# CPU e RAM
htop

# GPU
vcgencmd measure_temp
vcgencmd get_mem gpu
```

## Troubleshooting

### Problema: Interface lenta
- Verificar se aceleração de hardware está habilitada
- Reduzir resolução de vídeo das câmeras
- Diminuir taxa de atualização de sensores

### Problema: Dados de sensores não chegam
- Verificar conexão serial: `ls -l /dev/ttyUSB*`
- Testar comunicação: `screen /dev/ttyUSB0 115200`
- Verificar logs do backend

### Problema: GPS não funciona
- Verificar porta serial: `ls -l /dev/ttyAMA0`
- Testar NMEA: `cat /dev/ttyAMA0`
- Verificar antena GPS

## Próximas Melhorias

1. Implementar cache de dados com Redis
2. Adicionar sistema de alertas sonoros
3. Integrar reconhecimento de voz
4. Implementar machine learning para predição de falhas
5. Adicionar suporte a CAN Bus (OBD-II)
6. Implementar modo offline completo
7. Adicionar telemetria e analytics

## Conclusão

Este guia fornece todos os passos necessários para implementar o sistema de assistente de bordo em um ambiente de produção crítico. Siga cada etapa cuidadosamente e teste extensivamente antes de usar em condições reais de direção.

