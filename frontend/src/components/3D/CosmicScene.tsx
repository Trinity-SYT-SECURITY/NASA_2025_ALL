import React, { useRef, useMemo, useEffect } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Stars, Text, Sphere, Ring } from '@react-three/drei';
import * as THREE from 'three';

import ExoplanetSystem from './ExoplanetSystem';
import CosmicBackground from './CosmicBackground';
import ParticleField from './ParticleField';

interface CosmicSceneProps {
  exoplanets: any[];
  onPlanetClick: (planet: any) => void;
  selectedPlanet: any;
  filters: any;
}

const CosmicScene: React.FC<CosmicSceneProps> = ({
  exoplanets,
  onPlanetClick,
  selectedPlanet,
  filters
}) => {
  const { camera } = useThree();
  const controlsRef = useRef<any>();
  const sceneRef = useRef<THREE.Group>(null);

  // Camera animation for dramatic entrance
  useEffect(() => {
    if (camera) {
      camera.position.set(100, 50, 100);
      camera.lookAt(0, 0, 0);
    }
  }, [camera]);

  // Smooth camera transitions
  useFrame((state) => {
    if (controlsRef.current && selectedPlanet) {
      // Smooth zoom to selected planet
      const target = new THREE.Vector3(
        selectedPlanet.ra * 0.1,
        0,
        selectedPlanet.dec * 0.1
      );
      controlsRef.current.target.lerp(target, 0.05);
    }

    // Gentle scene rotation for dynamic feel
    if (sceneRef.current) {
      sceneRef.current.rotation.y += 0.001;
    }
  });

  // Process exoplanet positions for 3D space
  const processedExoplanets = useMemo(() => {
    return exoplanets.map((planet, index) => ({
      ...planet,
      position: [
        (planet.ra - 180) * 0.5, // Convert RA to X coordinate
        (Math.random() - 0.5) * 20, // Random Y for visual spread
        (planet.dec) * 0.5, // Convert Dec to Z coordinate
      ],
      color: getExoplanetColor(planet),
      scale: Math.log(planet.radius + 1) * 0.5 + 0.2,
    }));
  }, [exoplanets]);

  return (
    <group ref={sceneRef}>
      {/* Lighting Setup */}
      <ambientLight intensity={0.3} />
      <pointLight position={[0, 0, 0]} intensity={2} color="#ffffff" />
      <pointLight position={[50, 50, 50]} intensity={1} color="#00d4ff" />
      <pointLight position={[-50, -50, -50]} intensity={1} color="#ff6b35" />

      {/* Controls */}
      <OrbitControls
        ref={controlsRef}
        enablePan={true}
        enableZoom={true}
        enableRotate={true}
        minDistance={10}
        maxDistance={200}
        autoRotate={false}
        autoRotateSpeed={0.5}
        dampingFactor={0.05}
        enableDamping={true}
      />

      {/* Cosmic Background */}
      <CosmicBackground />

      {/* Particle Field */}
      <ParticleField count={2000} />

      {/* Starfield */}
      <Stars
        radius={300}
        depth={50}
        count={5000}
        factor={4}
        saturation={0}
        fade={true}
      />

      {/* Central Sun/Reference Point */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[2, 32, 32]} />
        <meshStandardMaterial
          color="#ffaa00"
          emissive="#ff4400"
          emissiveIntensity={0.8}
        />
      </mesh>

      {/* Sun Glow Effect */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[4, 32, 32]} />
        <meshBasicMaterial
          color="#ffaa00"
          transparent={true}
          opacity={0.2}
        />
      </mesh>

      {/* Coordinate Grid (subtle) */}
      <gridHelper
        args={[200, 20]}
        position={[0, -30, 0]}
        material={
          new THREE.LineBasicMaterial({
            color: 0x444444,
            transparent: true,
            opacity: 0.2,
          })
        }
      />

      {/* Exoplanet Systems */}
      {processedExoplanets.map((planet, index) => (
        <ExoplanetSystem
          key={planet.kepoi_name || index}
          planet={planet}
          position={planet.position}
          onClick={() => onPlanetClick(planet)}
          selected={selectedPlanet?.kepoi_name === planet.kepoi_name}
          scale={planet.scale}
          color={planet.color}
        />
      ))}

      {/* Information Labels for Notable Exoplanets */}
      {processedExoplanets
        .filter(p => p.habitability_score > 80)
        .slice(0, 5)
        .map((planet, index) => (
          <Text
            key={`label-${planet.kepoi_name}`}
            position={[
              planet.position[0],
              planet.position[1] + 3,
              planet.position[2]
            ]}
            fontSize={1}
            color="#00d4ff"
            anchorX="center"
            anchorY="middle"
            fillOpacity={0.8}
            outlineWidth={0.1}
            outlineColor="#000000"
          >
            {planet.kepler_name || planet.kepoi_name}
          </Text>
        ))}

      {/* Habitable Zone Visualization */}
      <Ring
        args={[15, 25, 64]}
        position={[0, 0, 0]}
        rotation={[-Math.PI / 2, 0, 0]}
      >
        <meshBasicMaterial
          color="#00ff88"
          transparent={true}
          opacity={0.1}
          side={THREE.DoubleSide}
        />
      </Ring>

      {/* Selection Indicator */}
      {selectedPlanet && (
        <mesh
          position={[
            (selectedPlanet.ra - 180) * 0.5,
            0,
            selectedPlanet.dec * 0.5
          ]}
        >
          <ringGeometry args={[3, 4, 32]} />
          <meshBasicMaterial
            color="#00d4ff"
            transparent={true}
            opacity={0.8}
          />
        </mesh>
      )}
    </group>
  );
};

// Helper function to determine exoplanet color based on properties
function getExoplanetColor(planet: any): string {
  // Color based on habitability score
  if (planet.habitability_score > 70) {
    return '#00ff88'; // Green for highly habitable
  } else if (planet.habitability_score > 40) {
    return '#ffaa00'; // Orange for moderately habitable
  } else if (planet.disposition === 'CONFIRMED') {
    return '#00d4ff'; // Blue for confirmed
  } else if (planet.disposition === 'CANDIDATE') {
    return '#ff6b35'; // Orange for candidates
  } else {
    return '#666666'; // Gray for false positives
  }
}

export default CosmicScene;
