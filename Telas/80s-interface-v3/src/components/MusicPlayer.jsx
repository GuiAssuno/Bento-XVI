import React, { useMemo } from 'react';

const MusicPlayer = React.memo(({ isPlaying, currentSong, nextSong }) => {
  const formatTime = useMemo(() => {
    return (seconds) => {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = Math.floor(seconds % 60);
      return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
    };
  }, []);

  if (!isPlaying) {
    return null;
  }

  const { title, artist, duration, playedTime } = currentSong;

  return (
    <div style={{
      position: 'absolute',
      bottom: 0,
      left: 0,
      right: 0,
      height: '80px',
      backgroundColor: 'rgba(0, 0, 0, 0.7)',
      color: '#00ffff',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 20px',
      boxSizing: 'border-box',
      zIndex: 100,
      borderTop: '2px solid #ff00ff',
      boxShadow: '0 -5px 15px rgba(255, 0, 255, 0.5)',
      willChange: 'transform', // Otimização de GPU
    }}>
      <div style={{ flex: 1, textAlign: 'left', fontSize: '0.8em' }}>
        {nextSong && `Próxima: ${nextSong.title} - ${nextSong.artist}`}
      </div>
      <div style={{ flex: 2, textAlign: 'center' }}>
        <div style={{ fontSize: '1.2em', fontWeight: 'bold' }}>{title}</div>
        <div style={{ fontSize: '1em' }}>{artist}</div>
      </div>
      <div style={{ flex: 1, textAlign: 'right', fontSize: '0.8em' }}>
        {formatTime(playedTime)} / {formatTime(duration)}
      </div>
    </div>
  );
});

MusicPlayer.displayName = 'MusicPlayer';

export default MusicPlayer;

