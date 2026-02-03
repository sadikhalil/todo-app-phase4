import React from 'react';
import { useTheme } from '../hooks/useTheme';
import { Moon, Sun } from 'lucide-react';
import { motion } from 'framer-motion';

const ThemeToggle: React.FC<{ className?: string }> = ({ className = '' }) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <motion.button
      onClick={toggleTheme}
      className={`p-2 rounded-full ${className} bg-orange text-white hover:bg-peach transition-colors`}
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
    >
      {theme === 'light' ? (
        <motion.div
          initial={{ rotate: -90, opacity: 0 }}
          animate={{ rotate: 0, opacity: 1 }}
          transition={{ duration: 0.2 }}
        >
          <Moon size={20} />
        </motion.div>
      ) : (
        <motion.div
          initial={{ rotate: 90, opacity: 0 }}
          animate={{ rotate: 0, opacity: 1 }}
          transition={{ duration: 0.2 }}
        >
          <Sun size={20} />
        </motion.div>
      )}
    </motion.button>
  );
};

export default ThemeToggle;