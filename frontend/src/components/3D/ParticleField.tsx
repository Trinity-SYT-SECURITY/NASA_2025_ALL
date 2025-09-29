import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface ParticleFieldProps {
  count: number;
}

const ParticleField: React.FC<ParticleFieldProps> = ({ count }) => {
  const pointsRef = useRef<THREE.Points>(null);

  const [positions, colors, sizes] = useMemo(() => {
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const sizes = new Float32Array(count);

    for (let i = 0; i < count; i++) {
      // Random positions in a large sphere
      const radius = Math.random() * 400 + 50;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);

      positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = radius * Math.cos(phi);

      // Random colors with cosmic theme
      const colorType = Math.random();
      if (colorType < 0.6) {
        // Blue-cyan particles
        colors[i * 3] = 0.2 + Math.random() * 0.3;     // R
        colors[i * 3 + 1] = 0.6 + Math.random() * 0.4; // G
        colors[i * 3 + 2] = 1;                          // B
      } else if (colorType < 0.8) {
        // Orange-red particles
        colors[i * 3] = 1;                              // R
        colors[i * 3 + 1] = 0.3 + Math.random() * 0.4; // G
        colors[i * 3 + 2] = 0.1 + Math.random() * 0.2; // B
      } else {
        // White particles
        colors[i * 3] = 1;     // R
        colors[i * 3 + 1] = 1; // G
        colors[i * 3 + 2] = 1; // B
      }

      sizes[i] = Math.random() * 3 + 0.5;
    }

    return [positions, colors, sizes];
  }, [count]);

  useFrame((state) => {
    if (pointsRef.current) {
      const time = state.clock.elapsedTime;
      
      // Gentle rotation
      pointsRef.current.rotation.y = time * 0.05;
      pointsRef.current.rotation.x = Math.sin(time * 0.1) * 0.1;
      
      // Update particle positions for floating effect
      const positions = pointsRef.current.geometry.attributes.position.array as Float32Array;
      const sizes = pointsRef.current.geometry.attributes.size.array as Float32Array;
      
      for (let i = 0; i < count; i++) {
        const i3 = i * 3;
        
        // Floating motion
        positions[i3 + 1] += Math.sin(time * 0.5 + i * 0.01) * 0.02;
        
        // Twinkling effect
        sizes[i] = (Math.sin(time * 2 + i * 0.1) * 0.5 + 1) * (Math.random() * 2 + 0.5);
      }
      
      pointsRef.current.geometry.attributes.position.needsUpdate = true;
      pointsRef.current.geometry.attributes.size.needsUpdate = true;
    }
  });

  const particleMaterial = useMemo(() => {
    return new THREE.PointsMaterial({
      size: 2,
      sizeAttenuation: true,
      vertexColors: true,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending,
    });
  }, []);

  return (
    <points ref={pointsRef} material={particleMaterial}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          array={positions}
          count={count}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          array={colors}
          count={count}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-size"
          array={sizes}
          count={count}
          itemSize={1}
        />
      </bufferGeometry>
    </points>
  );
};

export default ParticleField;
