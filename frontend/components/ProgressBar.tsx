import React from 'react';
import { useTodo } from '../contexts/TodoContext';
import { motion } from 'framer-motion';

interface ProgressBarProps {
  className?: string;
}

const ProgressBar: React.FC<ProgressBarProps> = ({ className = '' }) => {
  const { state } = useTodo();

  const completedCount = state.todos.filter(todo => todo.status === 'complete').length;
  const totalCount = state.todos.length;
  const percentage = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

  return (
    <div className={`w-full max-w-2xl ${className}`}>
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
          Progress: {percentage}%
        </span>
        <span className="text-sm text-gray-500 dark:text-gray-400">
          {completedCount} of {totalCount} completed
        </span>
      </div>
      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
        <motion.div
          className="bg-blue-500 h-2.5 rounded-full"
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5, ease: "easeInOut" }}
        ></motion.div>
      </div>
    </div>
  );
};

export default ProgressBar;