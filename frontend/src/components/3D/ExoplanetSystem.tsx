import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere, Ring, Text } from '@react-three/drei';
import * as THREE from 'three';

interface ExoplanetSystemProps {
  planet: any;
  position: [number, number, number];
  onClick: () => void;
  selected: boolean;
  scale: number;
  color: string;
}

const ExoplanetSystem: React.FC<ExoplanetSystemProps> = ({
  planet,
  position,
  onClick,
  selected,
  scale,
  color
}) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const ringRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);
  const orbitRef = useRef<THREE.Group>(null);

  // Animation parameters
  const orbitSpeed = useMemo(() => Math.random() * 0.01 + 0.005, []);
  const pulseSpeed = useMemo(() => Math.random() * 2 + 1, []);

  useFrame((state) => {
    const time = state.clock.getElapsedTime();

    // Planet rotation
    if (meshRef.current) {
      meshRef.current.rotation.y = time * 0.5;
      
      // Pulsing effect for high habitability planets
      if (planet.habitability_score > 70) {
        const pulse = Math.sin(time * pulseSpeed) * 0.1 + 1;
        meshRef.current.scale.setScalar(scale * pulse);
      }
    }

    // Selection ring animation
    if (ringRef.current && selected) {
      ringRef.current.rotation.z = time * 2;
      const ringPulse = Math.sin(time * 3) * 0.2 + 1;
      ringRef.current.scale.setScalar(ringPulse);
    }

    // Glow effect
    if (glowRef.current) {
      const glowPulse = Math.sin(time * 1.5) * 0.3 + 0.7;
      glowRef.current.material.opacity = glowPulse * 0.3;
    }

    // Orbital motion for moons/rings
    if (orbitRef.current) {
      orbitRef.current.rotation.y = time * orbitSpeed;
    }
  });

  // Create planet texture based on properties
  const planetTexture = useMemo(() => {
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 256;
    const ctx = canvas.getContext('2d')!;

    // Base color
    const baseColor = new THREE.Color(color);
    ctx.fillStyle = baseColor.getStyle();
    ctx.fillRect(0, 0, 256, 256);

    // Add surface features based on temperature
    if (planet.temperature < 300) {
      // Ice caps for cold planets
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, 256, 50);
      ctx.fillRect(0, 206, 256, 50);
    } else if (planet.temperature > 1000) {
      // Lava patterns for hot planets
      ctx.fillStyle = '#ff4400';
      for (let i = 0; i < 20; i++) {
        ctx.beginPath();
        ctx.arc(
          Math.random() * 256,
          Math.random() * 256,
          Math.random() * 20 + 5,
          0,
          Math.PI * 2
        );
        ctx.fill();
      }
    }

    // Atmosphere glow for habitable planets
    if (planet.habitability_score > 50) {
      const gradient = ctx.createRadialGradient(128, 128, 0, 128, 128, 128);
      gradient.addColorStop(0, 'rgba(0, 150, 255, 0.3)');
      gradient.addColorStop(1, 'rgba(0, 150, 255, 0)');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 256, 256);
    }

    return new THREE.CanvasTexture(canvas);
  }, [planet, color]);

  return (
    <group position={position}>
      {/* Main Planet */}
      <mesh
        ref={meshRef}
        onClick={(e) => {
          e.stopPropagation();
          onClick();
        }}
        scale={scale}
      >
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial
          map={planetTexture}
          emissive={color}
          emissiveIntensity={planet.habitability_score > 70 ? 0.2 : 0.1}
          roughness={0.8}
          metalness={0.2}
        />
      </mesh>

      {/* Glow Effect */}
      <mesh ref={glowRef} scale={scale * 1.5}>
        <sphereGeometry args={[1, 16, 16]} />
        <meshBasicMaterial
          color={color}
          transparent={true}
          opacity={0.2}
        />
      </mesh>

      {/* Selection Ring */}
      {selected && (
        <mesh ref={ringRef}>
          <ringGeometry args={[scale * 1.5, scale * 2, 32]} />
          <meshBasicMaterial
            color="#00d4ff"
            transparent={true}
            opacity={0.8}
            side={THREE.DoubleSide}
          />
        </mesh>
      )}

      {/* Orbital Elements */}
      <group ref={orbitRef}>
        {/* Rings for gas giants */}
        {planet.radius > 4 && (
          <mesh rotation={[-Math.PI / 4, 0, 0]}>
            <ringGeometry args={[scale * 1.2, scale * 1.8, 32]} />
            <meshBasicMaterial
              color={color}
              transparent={true}
              opacity={0.3}
              side={THREE.DoubleSide}
            />
          </mesh>
        )}

        {/* Moons for larger planets */}
        {planet.radius > 2 && (
          <group>
            <mesh position={[scale * 3, 0, 0]}>
              <sphereGeometry args={[scale * 0.2, 16, 16]} />
              <meshStandardMaterial color="#888888" />
            </mesh>
            {planet.radius > 6 && (
              <mesh position={[-scale * 4, 0, scale * 2]}>
                <sphereGeometry args={[scale * 0.15, 16, 16]} />
                <meshStandardMaterial color="#666666" />
              </mesh>
            )}
          </group>
        )}
      </group>

      {/* Habitability Indicator */}
      {planet.habitability_score > 70 && (
        <Text
          position={[0, scale + 1, 0]}
          fontSize={0.5}
          color="#00ff88"
          anchorX="center"
          anchorY="middle"
          fillOpacity={0.8}
        >
          ★ HABITABLE
        </Text>
      )}

      {/* Orbital Path (subtle) */}
      <mesh rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[
          Math.sqrt(planet.period || 10) * 2,
          Math.sqrt(planet.period || 10) * 2 + 0.1,
          64
        ]} />
        <meshBasicMaterial
          color="#444444"
          transparent={true}
          opacity={0.1}
          side={THREE.DoubleSide}
        />
      </mesh>
    </group>
  );
};

export default ExoplanetSystem;
