import React, { useMemo } from 'react';

const LoadingRing = React.memo(({ value = 0, max = 240, size = 100, strokeWidth = 10 }) => {
  // Memoizar cálculos para evitar recalcular em cada render
  const { radius, circumference, offset, strokeColor } = useMemo(() => {
    const r = (size - strokeWidth) / 2;
    const circ = 2 * Math.PI * r;
    const off = circ - (value / max) * circ;

    let color = '#00FF00'; // Verde padrão
    if (value > max * 0.75) {
      color = '#FFD700'; // Amarelo para valores altos
    }
    if (value === max) {
      color = '#FF0000'; // Vermelho para perigo/máximo
    }

    return { radius: r, circumference: circ, offset: off, strokeColor: color };
  }, [value, max, size, strokeWidth]);

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle
        stroke="#333"
        fill="transparent"
        strokeWidth={strokeWidth}
        r={radius}
        cx={size / 2}
        cy={size / 2}
      />
      <circle
        stroke={strokeColor}
        fill="transparent"
        strokeWidth={strokeWidth}
        strokeDasharray={`${circumference} ${circumference}`}
        strokeDashoffset={offset}
        r={radius}
        cx={size / 2}
        cy={size / 2}
        style={{
          transition: 'stroke-dashoffset 0.3s ease-in-out, stroke 0.3s ease-in-out',
          transform: 'rotate(-90deg)',
          transformOrigin: '50% 50%',
          willChange: 'stroke-dashoffset, stroke', // Otimização de GPU
        }}
      />
      <text
        x="50%"
        y="50%"
        textAnchor="middle"
        dominantBaseline="middle"
        fill="white"
        fontSize={size / 5}
        fontFamily="'Press Start 2P', cursive, monospace"
      >
        {value}
      </text>
    </svg>
  );
});

LoadingRing.displayName = 'LoadingRing';

export default LoadingRing;

