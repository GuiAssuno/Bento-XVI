/**
 * Frontend da Assistente de Bordo - JavaScript Principal
 * Gerencia a comunicação com o backend e atualiza a interface
 */

const API_BASE_URL = 'http://localhost:5000/api';

class AssistenteBordoFrontend {
    constructor() {
        this.rings = [
            { element: document.getElementById('ring1-progress'), value: document.getElementById('ring1-value'), current: 0, max: 120, unit: '°C', key: 'temperatura_motor_ect' },
            { element: document.getElementById('ring2-progress'), value: document.getElementById('ring2-value'), current: 0, max: 8000, unit: '', key: 'posicao_virabrequim_ckp' },
            { element: document.getElementById('ring3-progress'), value: document.getElementById('ring3-value'), current: 0, max: 100, unit: '%', key: 'fuel' }
        ];
        
        this.videoDisplay = document.getElementById('videoDisplay');
        this.musicPlayer = document.getElementById('musicPlayer');
        this.frequencyDisplay = document.getElementById('frequencyDisplay');
        this.menuOverlay = document.getElementById('menuOverlay');
        this.homeButton = document.getElementById('homeButton');
        this.closeMenu = document.getElementById('closeMenu');
        this.voiceIndicator = document.getElementById('voiceIndicator');
        this.commandInput = document.getElementById('commandInput');
        this.sendCommandBtn = document.getElementById('sendCommandBtn');
        this.responseText = document.getElementById('responseText');
        
        this.init();
    }

    init() {
        this.createFrequencyBars();
        this.setupEventListeners();
        this.startDataPolling();
    }

    setupEventListeners() {
        // Home button click
        this.homeButton.addEventListener('click', () => {
            this.toggleMenu();
        });

        // Close menu button
        this.closeMenu.addEventListener('click', () => {
            this.toggleMenu();
        });

        // Close menu when clicking outside
        this.menuOverlay.addEventListener('click', (e) => {
            if (e.target === this.menuOverlay) {
                this.toggleMenu();
            }
        });

        // Menu item clicks
        document.querySelectorAll('.menu-item').forEach(item => {
            item.addEventListener('click', () => {
                const func = item.getAttribute('data-function');
                this.handleMenuFunction(func);
            });
        });

        // Command input
        if (this.sendCommandBtn) {
            this.sendCommandBtn.addEventListener('click', () => {
                this.sendCommand();
            });
        }

        if (this.commandInput) {
            this.commandInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.sendCommand();
                }
            });
        }

        // Voice command simulation (press 'M' key)
        document.addEventListener('keydown', (e) => {
            if (e.key === 'm' || e.key === 'M') {
                this.showVoiceIndicator();
                setTimeout(() => {
                    this.toggleMenu();
                }, 500);
            }
        });
    }

    toggleMenu() {
        this.menuOverlay.classList.toggle('active');
    }

    async handleMenuFunction(func) {
        console.log(`Função selecionada: ${func}`);
        
        try {
            switch(func) {
                case 'music':
                    await this.toggleMusic();
                    this.showMusicPlayer(true);
                    break;
                case 'camera':
                    this.showVideo(true);
                    await this.updateCameraData();
                    break;
                case 'lights':
                    await this.toggleLights();
                    break;
                case 'engine':
                    await this.updateMotorData();
                    break;
                default:
                    console.log(`Função ${func} não implementada ainda`);
            }
        } catch (error) {
            console.error('Erro ao executar função:', error);
        }
        
        this.toggleMenu();
    }

    showVoiceIndicator() {
        this.voiceIndicator.classList.add('active');
        setTimeout(() => {
            this.voiceIndicator.classList.remove('active');
        }, 2000);
    }

    createFrequencyBars() {
        const barCount = Math.floor(this.frequencyDisplay.offsetWidth / 6);
        for (let i = 0; i < barCount; i++) {
            const bar = document.createElement('div');
            bar.className = 'freq-bar';
            bar.style.height = '2px';
            bar.style.animationDelay = `${i * 0.05}s`;
            this.frequencyDisplay.appendChild(bar);
        }
    }

    updateRing(ringIndex, value) {
        if (ringIndex < 0 || ringIndex >= this.rings.length) return;
        
        const ring = this.rings[ringIndex];
        const circumference = 2 * Math.PI * 36;
        const progress = (value / ring.max) * circumference;
        
        // Color transition based on value percentage
        let color = '#00ffff';
        const percentage = (value / ring.max) * 100;
        if (percentage > 80) color = '#ff6600';
        else if (percentage > 60) color = '#ffff00';
        else if (percentage > 40) color = '#00ff00';
        
        ring.element.style.stroke = color;
        ring.element.style.strokeDasharray = `${progress} ${circumference}`;
        
        // Format value display
        let displayValue = Math.round(value);
        if (ringIndex === 1) { // RPM
            displayValue = Math.round(value / 100); // Display as RPM x100
        }
        
        ring.value.textContent = displayValue + ring.unit;
        ring.value.style.color = color;
        ring.current = value;
    }

    showVideo(show = true) {
        if (show) {
            this.videoDisplay.classList.add('active');
        } else {
            this.videoDisplay.classList.remove('active');
        }
    }

    showMusicPlayer(show = true) {
        if (show) {
            this.musicPlayer.classList.add('active');
        } else {
            this.musicPlayer.classList.remove('active');
        }
    }

    animateFrequencyBars() {
        const bars = this.frequencyDisplay.querySelectorAll('.freq-bar');
        bars.forEach((bar, index) => {
            const height = Math.random() * 60 + 5;
            bar.style.height = `${height}px`;
        });
    }

    // API Communication Methods

    async fetchStatus() {
        try {
            const response = await fetch(`${API_BASE_URL}/status`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Erro ao buscar status:', error);
            return null;
        }
    }

    async updateMotorData() {
        try {
            const response = await fetch(`${API_BASE_URL}/motor`);
            const motorData = await response.json();
            
            if (motorData) {
                // Update ring 1 - Temperature
                if (motorData.temperatura_motor_ect !== undefined) {
                    this.updateRing(0, motorData.temperatura_motor_ect);
                }
                
                // Update ring 2 - RPM (using CKP as proxy)
                if (motorData.posicao_virabrequim_ckp !== undefined) {
                    // Convert CKP position (0-360) to RPM estimate (0-8000)
                    const rpm = (motorData.posicao_virabrequim_ckp / 360) * 8000;
                    this.updateRing(1, rpm);
                }
                
                // Update ring 3 - Fuel (simulated)
                // In a real system, this would come from a fuel sensor
                const currentFuel = this.rings[2].current || 75;
                this.updateRing(2, Math.max(0, currentFuel - 0.01));
            }
        } catch (error) {
            console.error('Erro ao atualizar dados do motor:', error);
        }
    }

    async sendCommand() {
        const command = this.commandInput.value.trim();
        if (!command) return;

        this.showVoiceIndicator();

        try {
            const response = await fetch(`${API_BASE_URL}/command`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: command })
            });
            
            const data = await response.json();
            
            if (this.responseText) {
                this.responseText.textContent = data.response || 'Sem resposta';
                this.responseText.style.display = 'block';
                setTimeout(() => {
                    this.responseText.style.display = 'none';
                }, 5000);
            }
            
            this.commandInput.value = '';
        } catch (error) {
            console.error('Erro ao enviar comando:', error);
            if (this.responseText) {
                this.responseText.textContent = 'Erro ao processar comando';
            }
        }
    }

    async toggleLights() {
        try {
            const response = await fetch(`${API_BASE_URL}/lights`, {
                method: 'POST'
            });
            const data = await response.json();
            console.log(data.response);
            if (this.responseText) {
                this.responseText.textContent = data.response;
            }
        } catch (error) {
            console.error('Erro ao alternar luzes:', error);
        }
    }

    async toggleMusic() {
        try {
            const response = await fetch(`${API_BASE_URL}/music`, {
                method: 'POST'
            });
            const data = await response.json();
            console.log(data.response);
            if (this.responseText) {
                this.responseText.textContent = data.response;
            }
        } catch (error) {
            console.error('Erro ao alternar música:', error);
        }
    }

    async updateCameraData() {
        try {
            const response = await fetch(`${API_BASE_URL}/camera`);
            const data = await response.json();
            console.log('Visão Computacional:', data);
        } catch (error) {
            console.error('Erro ao atualizar dados da câmera:', error);
        }
    }

    startDataPolling() {
        // Update motor data every 500ms
        setInterval(() => {
            this.updateMotorData();
        }, 500);

        // Animate frequency bars
        setInterval(() => {
            this.animateFrequencyBars();
        }, 80);

        // Show music player after 2 seconds
        setTimeout(() => {
            this.showMusicPlayer(true);
        }, 2000);

        // Show video after 3 seconds
        setTimeout(() => {
            this.showVideo(true);
        }, 3000);
    }
}

// Start application when page loads
window.addEventListener('load', () => {
    window.assistenteBordo = new AssistenteBordoFrontend();
});

// Handle resize
window.addEventListener('resize', () => {
    if (window.assistenteBordo) {
        window.assistenteBordo.frequencyDisplay.innerHTML = '';
        window.assistenteBordo.createFrequencyBars();
    }
});

