import React from 'react';
import { motion } from 'framer-motion';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'elevated' | 'outline';
  animated?: boolean;
  initial?: any;
  animate?: any;
  transition?: any;
}

const Card: React.FC<CardProps> = ({
  children,
  className = '',
  variant = 'default',
  animated = false,
  initial = { opacity: 0, y: 20 },
  animate = { opacity: 1, y: 0 },
  transition = { duration: 0.3 },
}) => {
  const baseClasses = 'rounded-xl border';

  const variantClasses = {
    default: 'bg-white border-gray-200 dark:bg-gray-800 dark:border-gray-700',
    elevated: 'bg-white border-gray-200 shadow-lg dark:bg-gray-800 dark:border-gray-700',
    outline: 'bg-transparent border-gray-300 dark:border-gray-600',
  };

  const classes = `${baseClasses} ${variantClasses[variant]} ${className}`;

  if (animated) {
    return (
      <motion.div
        className={classes}
        initial={initial}
        animate={animate}
        transition={transition}
      >
        {children}
      </motion.div>
    );
  }

  return <div className={classes}>{children}</div>;
};

export default Card;