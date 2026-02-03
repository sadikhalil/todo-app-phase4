import React from 'react';
import { useTodo } from '../contexts/TodoContext';
import { motion } from 'framer-motion';

const TodoFilters: React.FC = () => {
  const { state, setFilter } = useTodo();

  const filters = [
    { id: 'all', label: 'All' },
    { id: 'active', label: 'Active' },
    { id: 'completed', label: 'Completed' },
  ];

  return (
    <div className="flex space-x-2 mb-6">
      {filters.map((filter) => (
        <motion.button
          key={filter.id}
          onClick={() => setFilter(filter.id as 'all' | 'active' | 'completed')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            state.filter === filter.id
              ? 'bg-blue-500 text-white shadow-md'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
          }`}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {filter.label}
        </motion.button>
      ))}
    </div>
  );
};

export default TodoFilters;