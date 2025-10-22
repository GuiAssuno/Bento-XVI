import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import LoadingRing from './components/LoadingRing';
import VideoPlayer from './components/VideoPlayer';
import AudioVisualizer from './components/AudioVisualizer';
import MusicPlayer from './components/MusicPlayer';
import GpsMap from './components/GpsMap';
import './App.css';

function App() {
  // Estado para os anéis de carga (simulando dados de sensores)
  const [loadValue1, setLoadValue1] = useState(0);
  const [loadValue2, setLoadValue2] = useState(0);
  const [loadValue3, setLoadValue3] = useState(0);
  
  // Estado para vídeo
  const [isTransmittingVideo, setIsTransmittingVideo] = useState(false);
  const videoSource = useMemo(() => "https://www.w3schools.com/html/mov_bbb.mp4", []);
  
  // Estado para áudio
  const [isTransmittingSound, setIsTransmittingSound] = useState(false);
  const [frequencies, setFrequencies] = useState([]);
  
  // Estado para música
  const [isPlayingMusic, setIsPlayingMusic] = useState(false);
  const [currentSong, setCurrentSong] = useState({
    title: 'Synthwave Dream',
    artist: 'Neon Rider',
    duration: 240,
    playedTime: 0,
  });
  const nextSong = useMemo(() => ({
    title: 'Electric Night',
    artist: 'Cyber Runner',
  }), []);
  
  // Estado para GPS
  const [latitude, setLatitude] = useState(-23.55052);
  const [longitude, setLongitude] = useState(-46.633309);

  // Refs para intervalos (evitar memory leaks)
  const intervalsRef = useRef([]);

  // Simulação de anéis de carga (substituir por dados reais dos sensores ESP32)
  useEffect(() => {
    const interval1 = setInterval(() => {
      setLoadValue1(prev => (prev >= 240 ? 0 : prev + 1));
    }, 50);
    
    const interval2 = setInterval(() => {
      setLoadValue2(prev => (prev >= 240 ? 0 : prev + 2));
    }, 70);
    
    const interval3 = setInterval(() => {
      setLoadValue3(prev => (prev >= 240 ? 0 : prev + 3));
    }, 90);

    intervalsRef.current.push(interval1, interval2, interval3);

    return () => {
      intervalsRef.current.forEach(clearInterval);
      intervalsRef.current = [];
    };
  }, []);

  // Simulação de transmissão de vídeo (substituir por stream IP real)
  useEffect(() => {
    const videoTimer = setTimeout(() => {
      setIsTransmittingVideo(true);
    }, 3000);

    return () => clearTimeout(videoTimer);
  }, []);

  // Simulação de áudio e música (substituir por Web Audio API real)
  useEffect(() => {
    const soundTimer = setTimeout(() => {
      setIsTransmittingSound(true);
      setIsPlayingMusic(true);
    }, 5000);

    const musicProgress = setInterval(() => {
      setCurrentSong(prev => {
        if (prev.playedTime >= prev.duration) {
          return { ...prev, playedTime: 0 };
        }
        return { ...prev, playedTime: prev.playedTime + 1 };
      });
    }, 1000);

    // Otimização: usar requestAnimationFrame para frequências
    let animationFrameId;
    const updateFrequencies = () => {
      if (isTransmittingSound) {
        setFrequencies(Array.from({ length: 50 }, () => Math.random()));
      }
      animationFrameId = requestAnimationFrame(updateFrequencies);
    };
    
    if (isTransmittingSound) {
      updateFrequencies();
    }

    return () => {
      clearTimeout(soundTimer);
      clearInterval(musicProgress);
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
      }
    };
  }, [isTransmittingSound]);

  // Simulação de GPS (substituir por Geolocation API real)
  useEffect(() => {
    const gpsInterval = setInterval(() => {
      setLatitude(prev => prev + (Math.random() - 0.5) * 0.001);
      setLongitude(prev => prev + (Math.random() - 0.5) * 0.001);
    }, 5000);

    return () => clearInterval(gpsInterval);
  }, []);

  return (
    <div className="app-container">
      <div className="top-right-rings-container">
        <div className="ring-top-right">
          <LoadingRing value={loadValue1} size={80} strokeWidth={8} />
        </div>
        <div className="ring-top-left-of-right">
          <LoadingRing value={loadValue2} size={80} strokeWidth={8} />
        </div>
        <div className="ring-bottom-of-right">
          <LoadingRing value={loadValue3} size={80} strokeWidth={8} />
        </div>
      </div>

      <GpsMap latitude={latitude} longitude={longitude} />

      <VideoPlayer isTransmitting={isTransmittingVideo} videoSource={videoSource} />

      <AudioVisualizer isTransmittingSound={isTransmittingSound} frequencies={frequencies} />

      <MusicPlayer isPlaying={isPlayingMusic} currentSong={currentSong} nextSong={nextSong} />
    </div>
  );
}

export default App;

