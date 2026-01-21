import React from 'react';

const VideoPlayer = React.memo(({ isTransmitting, videoSource }) => {
  if (!isTransmitting) {
    return null;
  }

  return (
    <div style={{
      width: '80%',
      height: '60%',
      backgroundColor: '#000000',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      border: '2px solid #00ffff',
      boxShadow: '0 0 15px #00ffff, 0 0 20px #00ffff inset',
      position: 'absolute',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      zIndex: 10,
      willChange: 'transform', // Otimização de GPU
    }}>
      <video
        src={videoSource}
        controls
        autoPlay
        loop
        muted // Importante para autoplay em navegadores modernos
        playsInline // Importante para mobile
        preload="auto" // Pré-carregar vídeo
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
        }}
      >
        Seu navegador não suporta a tag de vídeo.
      </video>
    </div>
  );
});

VideoPlayer.displayName = 'VideoPlayer';

export default VideoPlayer;

