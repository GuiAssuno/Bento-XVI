import React, { useRef, useEffect, useCallback } from 'react';

const AudioVisualizer = React.memo(({ isTransmittingSound, frequencies }) => {
  const canvasRef = useRef(null);
  const animationFrameRef = useRef(null);

  // Função de desenho otimizada com requestAnimationFrame
  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d', { alpha: false }); // Desabilitar alpha para performance
    const width = canvas.width;
    const height = canvas.height;

    // Limpar canvas de forma eficiente
    ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
    ctx.fillRect(0, 0, width, height);

    if (isTransmittingSound && frequencies && frequencies.length > 0) {
      const barWidth = width / frequencies.length;
      
      // Criar gradiente uma vez
      const gradient = ctx.createLinearGradient(0, 0, width, 0);
      gradient.addColorStop(0, '#00ffff');
      gradient.addColorStop(0.5, '#ff00ff');
      gradient.addColorStop(1, '#ffff00');
      
      ctx.fillStyle = gradient;

      // Desenhar barras de forma eficiente
      for (let i = 0; i < frequencies.length; i++) {
        const barHeight = frequencies[i] * height;
        const x = i * (barWidth + 1);
        ctx.fillRect(x, height - barHeight, barWidth, barHeight);
      }
    } else {
      // Desenhar linhas estáticas quando não há som
      ctx.strokeStyle = '#00ffff';
      ctx.lineWidth = 2;

      for (let i = 0; i < 10; i++) {
        const y = (height / 10) * i + (height / 20);
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }
    }
  }, [isTransmittingSound, frequencies]);

  useEffect(() => {
    const animate = () => {
      draw();
      animationFrameRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [draw]);

  return (
    <canvas
      ref={canvasRef}
      width={window.innerWidth}
      height={window.innerHeight * 0.2}
      style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        zIndex: 5,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
      }}
    />
  );
});

AudioVisualizer.displayName = 'AudioVisualizer';

export default AudioVisualizer;

