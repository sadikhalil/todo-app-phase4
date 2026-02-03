import React from 'react';
import { useTodo } from '../contexts/TodoContext';
import TodoItem from './TodoItem';
import { AnimatePresence } from 'framer-motion';

const TodoList: React.FC = () => {
  const { state, toggleTodo, deleteTodo, updateTodo } = useTodo();

  // Filter todos based on the current filter
  const filteredTodos = state.todos.filter(todo => {
    if (state.filter === 'active') return todo.status !== 'complete';
    if (state.filter === 'completed') return todo.status === 'complete';
    return true; // 'all'
  });

  return (
    <div className="w-full max-w-2xl">
      <AnimatePresence>
        {filteredTodos.length > 0 ? (
          <ul className="space-y-3">
            <AnimatePresence>
              {filteredTodos.map(todo => (
                <TodoItem
                  key={todo.id}
                  todo={todo}
                  onToggle={toggleTodo}
                  onDelete={deleteTodo}
                  onEdit={updateTodo}
                />
              ))}
            </AnimatePresence>
          </ul>
        ) : (
          <div className="text-center py-12">
            <div className="text-gray-500 dark:text-gray-400 text-lg">
              {state.filter === 'completed'
                ? 'No completed tasks yet'
                : state.filter === 'active'
                  ? 'No active tasks'
                  : 'Add your first task to get started!'}
            </div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default TodoList;