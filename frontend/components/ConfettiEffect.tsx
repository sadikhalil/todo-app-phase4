import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

interface ConfettiPiece {
  id: number;
  x: number;
  y: number;
  size: number;
  color: string;
  rotation: number;
  duration: number;
  delay: number;
}

interface ConfettiEffectProps {
  isActive: boolean;
  particleCount?: number;
  spread?: number;
  colors?: string[];
}

const ConfettiEffect: React.FC<ConfettiEffectProps> = ({
  isActive,
  particleCount = 50,
  spread = 180,
  colors = ['#f44336', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3', '#03a9f4', '#00bcd4', '#009688', '#4CAF50']
}) => {
  const [particles, setParticles] = React.useState<ConfettiPiece[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isActive) {
      const newParticles: ConfettiPiece[] = [];

      for (let i = 0; i < particleCount; i++) {
        newParticles.push({
          id: i,
          x: 50 + (Math.random() - 0.5) * 10, // Start near center
          y: 50,
          size: 5 + Math.random() * 10,
          color: colors[Math.floor(Math.random() * colors.length)],
          rotation: Math.random() * 360,
          duration: 1 + Math.random() * 2,
          delay: Math.random() * 0.5,
        });
      }

      setParticles(newParticles);
    } else {
      setParticles([]);
    }
  }, [isActive, particleCount, spread, colors]);

  if (!isActive || particles.length === 0) {
    return null;
  }

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 pointer-events-none z-50 overflow-hidden"
    >
      {particles.map((particle) => (
        <motion.div
          key={particle.id}
          className="absolute rounded-sm"
          initial={{
            left: `${particle.x}%`,
            top: `${particle.y}%`,
            width: `${particle.size}px`,
            height: `${particle.size}px`,
            backgroundColor: particle.color,
            rotate: particle.rotation,
          }}
          animate={{
            left: [
              `${particle.x}%`,
              `${particle.x + Math.cos(particle.rotation * Math.PI / 180) * 50}%`,
            ],
            top: [
              `${particle.y}%`,
              `${particle.y - 100}%`,
            ],
            rotate: particle.rotation + 360,
            opacity: [1, 1, 0],
          }}
          transition={{
            duration: particle.duration,
            delay: particle.delay,
            ease: "easeOut",
          }}
        />
      ))}
    </div>
  );
};

export default ConfettiEffect;