import React from 'react';
import { motion } from 'framer-motion';

interface AnimatedWrapperProps {
  children: React.ReactNode;
  animationType?: 'fadeIn' | 'slideIn' | 'bounce' | 'scaleIn' | 'stagger';
  delay?: number;
  duration?: number;
  easing?: 'easeInOut' | 'easeOut' | 'easeIn' | 'circInOut';
  trigger?: boolean;
  className?: string;
  direction?: 'left' | 'right' | 'up' | 'down';
}

const AnimatedWrapper: React.FC<AnimatedWrapperProps> = ({
  children,
  animationType = 'fadeIn',
  delay = 0,
  duration = 0.5,
  easing = 'easeInOut',
  trigger = true,
  className = '',
  direction = 'up',
}) => {
  const getAnimationProps = () => {
    const easingMap = {
      easeInOut: [0.4, 0, 0.2, 1],
      easeOut: [0.2, 0.6, 0.2, 1],
      easeIn: [0.4, 0, 1, 1],
      circInOut: [0.85, 0, 0.15, 1],
    };

    const commonProps = {
      initial: animationType === 'fadeIn' ? { opacity: 0 } :
                animationType === 'slideIn' ?
                  direction === 'left' ? { opacity: 0, x: -50 } :
                  direction === 'right' ? { opacity: 0, x: 50 } :
                  direction === 'up' ? { opacity: 0, y: 50 } : { opacity: 0, y: -50 } :
                animationType === 'scaleIn' ? { opacity: 0, scale: 0.8 } :
                animationType === 'bounce' ? { opacity: 0, y: 50, scale: 0.8 } : { opacity: 0 },
      animate: trigger ? {
        opacity: 1,
        x: animationType === 'slideIn' && (direction === 'left' || direction === 'right') ? 0 : undefined,
        y: animationType === 'slideIn' && (direction === 'up' || direction === 'down') ? 0 :
           animationType === 'bounce' ? [-50, 0, -10, 0] : undefined,
        scale: animationType === 'scaleIn' || animationType === 'bounce' ? 1 : undefined,
      } : {},
      exit: animationType === 'fadeIn' || animationType === 'slideIn' || animationType === 'scaleIn' ?
             animationType === 'slideIn' ?
               direction === 'left' ? { opacity: 0, x: -50 } :
               direction === 'right' ? { opacity: 0, x: 50 } :
               direction === 'up' ? { opacity: 0, y: 50 } : { opacity: 0, y: -50 } :
             animationType === 'scaleIn' ? { opacity: 0, scale: 0.8 } : { opacity: 0 } : {},
      transition: animationType === 'bounce' ? {
        duration,
        delay,
        ease: easingMap[easing],
        type: 'spring',
        stiffness: 300,
        damping: 20,
      } : {
        duration,
        delay,
        ease: easingMap[easing],
        type: 'tween',
      } as any,
    };

    return commonProps;
  };

  return (
    <motion.div
      className={className}
      {...getAnimationProps()}
    >
      {children}
    </motion.div>
  );
};

export default AnimatedWrapper;