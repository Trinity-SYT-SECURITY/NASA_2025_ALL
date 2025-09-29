import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

const CosmicBackground: React.FC = () => {
  const meshRef = useRef<THREE.Mesh>(null);

  // Create nebula-like background texture
  const backgroundTexture = useMemo(() => {
    const canvas = document.createElement('canvas');
    canvas.width = 1024;
    canvas.height = 1024;
    const ctx = canvas.getContext('2d')!;

    // Create gradient background
    const gradient = ctx.createRadialGradient(512, 512, 0, 512, 512, 512);
    gradient.addColorStop(0, 'rgba(0, 50, 100, 0.8)');
    gradient.addColorStop(0.3, 'rgba(50, 0, 100, 0.6)');
    gradient.addColorStop(0.6, 'rgba(100, 0, 50, 0.4)');
    gradient.addColorStop(1, 'rgba(0, 0, 0, 0.9)');
    
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 1024, 1024);

    // Add nebula clouds
    for (let i = 0; i < 20; i++) {
      const x = Math.random() * 1024;
      const y = Math.random() * 1024;
      const radius = Math.random() * 200 + 50;
      
      const cloudGradient = ctx.createRadialGradient(x, y, 0, x, y, radius);
      cloudGradient.addColorStop(0, `rgba(${Math.random() * 100 + 100}, ${Math.random() * 100 + 50}, ${Math.random() * 200 + 100}, 0.3)`);
      cloudGradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
      
      ctx.fillStyle = cloudGradient;
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fill();
    }

    // Add stars
    for (let i = 0; i < 500; i++) {
      const x = Math.random() * 1024;
      const y = Math.random() * 1024;
      const brightness = Math.random();
      
      ctx.fillStyle = `rgba(255, 255, 255, ${brightness})`;
      ctx.beginPath();
      ctx.arc(x, y, Math.random() * 2 + 0.5, 0, Math.PI * 2);
      ctx.fill();
    }

    return new THREE.CanvasTexture(canvas);
  }, []);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.1) * 0.1;
      meshRef.current.rotation.y += 0.001;
    }
  });

  return (
    <mesh ref={meshRef} position={[0, 0, -300]}>
      <sphereGeometry args={[500, 32, 32]} />
      <meshBasicMaterial
        map={backgroundTexture}
        side={THREE.BackSide}
        transparent={true}
        opacity={0.8}
      />
    </mesh>
  );
};

export default CosmicBackground;
