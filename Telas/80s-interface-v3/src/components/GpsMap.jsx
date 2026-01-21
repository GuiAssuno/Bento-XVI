import React, { useMemo } from 'react';

const GpsMap = React.memo(({ latitude = -23.55052, longitude = -46.633309 }) => {
  const mapUrl = useMemo(() => {
    return `https://maps.google.com/maps?q=${latitude},${longitude}&hl=pt-BR&z=14&output=embed`;
  }, [latitude, longitude]);

  return (
    <div style={{
      position: 'absolute',
      top: '20px',
      left: '20px',
      width: '250px',
      height: '150px',
      border: '2px solid #00ffff',
      boxShadow: '0 0 10px #00ffff, 0 0 15px #00ffff inset',
      zIndex: 100,
      overflow: 'hidden',
      backgroundColor: '#000',
      willChange: 'transform', // Otimização de GPU
    }}>
      <iframe
        title="GPS Location"
        width="100%"
        height="100%"
        frameBorder="0"
        style={{ border: 0 }}
        src={mapUrl}
        allowFullScreen=""
        aria-hidden="false"
        tabIndex="0"
        loading="lazy" // Lazy loading para performance
      ></iframe>
      <div style={{
        position: 'absolute',
        bottom: '5px',
        left: '5px',
        color: '#ff00ff',
        fontSize: '0.7em',
        fontFamily: "'Press Start 2P', cursive, monospace",
        textShadow: '0 0 5px #000',
      }}>
        LAT: {latitude.toFixed(4)} LON: {longitude.toFixed(4)}
      </div>
    </div>
  );
});

GpsMap.displayName = 'GpsMap';

export default GpsMap;

