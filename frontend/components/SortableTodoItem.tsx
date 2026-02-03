import React, { useState, useEffect } from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { motion } from 'framer-motion';
import { Trash2, CheckCircle, Circle, GripVertical } from 'lucide-react';
import { Todo } from '../types/todo';
import ConfettiEffect from './ConfettiEffect';
import Button from './ui/Button';

interface SortableTodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
  onEdit: (id: string, text: string) => void;
}

const SortableTodoItem: React.FC<SortableTodoItemProps> = ({ todo, onToggle, onDelete, onEdit }) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: todo.id });

  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(todo.text);
  const [showConfetti, setShowConfetti] = useState(false);
  const [wasIncomplete, setWasIncomplete] = useState(todo.status !== 'complete');

  useEffect(() => {
    // Show confetti when a task is completed (but not when it becomes incomplete again)
    if (todo.status === 'complete' && wasIncomplete) {
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 2000); // Hide confetti after 2 seconds
      setWasIncomplete(false);
    } else if (todo.status !== 'complete') {
      setWasIncomplete(true);
    }
  }, [todo.status, wasIncomplete]);

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
    zIndex: isDragging ? 1000 : 1,
  };

  const handleEdit = () => {
    if (isEditing) {
      onEdit(todo.id, editText);
    }
    setIsEditing(!isEditing);
  };

  const handleCancelEdit = () => {
    setEditText(todo.text);
    setIsEditing(false);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onEdit(todo.id, editText);
    setIsEditing(false);
  };

  return (
    <>
      {showConfetti && <ConfettiEffect isActive={true} />}
      <motion.div
        ref={setNodeRef}
        style={style}
        layout
        initial={{ opacity: 0, x: 100, scale: 0.8 }}
        animate={{ opacity: 1, x: 0, scale: 1 }}
        exit={{ opacity: 0, x: -100, height: 0, scale: 0.8 }}
        transition={{ duration: 0.3, ease: "easeOut" }}
        className="flex items-center justify-between p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 border border-gray-200 dark:border-gray-700"
      >
        <div className="flex items-center space-x-3 flex-1 min-w-0">
          <motion.button
            {...attributes}
            {...listeners}
            className="flex-shrink-0 cursor-grab active:cursor-grabbing"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            aria-label="Drag to reorder"
          >
            <GripVertical className="text-gray-400" size={20} />
          </motion.button>

          <motion.button
            onClick={() => onToggle(todo.id)}
            className="flex-shrink-0"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            aria-label={todo.status === 'complete' ? "Mark as incomplete" : "Mark as complete"}
          >
            {todo.status === 'complete' ? (
              <motion.div
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                exit={{ scale: 0, rotate: 180 }}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
              >
                <CheckCircle className="text-green-500" size={24} />
              </motion.div>
            ) : (
              <motion.div
                initial={{ scale: 0, rotate: 180 }}
                animate={{ scale: 1, rotate: 0 }}
                exit={{ scale: 0, rotate: -180 }}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
              >
                <Circle className="text-gray-400" size={24} />
              </motion.div>
            )}
          </motion.button>

          {isEditing ? (
            <form onSubmit={handleSubmit} className="flex-1 min-w-0">
              <input
                type="text"
                value={editText}
                onChange={(e) => setEditText(e.target.value)}
                className="w-full bg-transparent border-b border-gray-300 dark:border-gray-600 focus:outline-none focus:border-blue-500 dark:focus:border-blue-400 pb-1"
                autoFocus
              />
              <div className="flex space-x-2 mt-2">
                <Button size="sm" type="submit">Save</Button>
                <Button size="sm" variant="ghost" onClick={handleCancelEdit}>Cancel</Button>
              </div>
            </form>
          ) : (
            <motion.span
              className={`flex-1 min-w-0 break-words ${todo.status === 'complete' ? 'line-through text-gray-500 dark:text-gray-500' : 'text-gray-800 dark:text-gray-200'}`}
              animate={{
                textDecoration: todo.status === 'complete' ? 'line-through' : 'none',
                color: todo.status === 'complete' ? '#9CA3AF' : '#1F2937'
              }}
              transition={{ duration: 0.3 }}
            >
              {todo.text}
            </motion.span>
          )}
        </div>

        <div className="flex items-center space-x-2 ml-4">
          {!isEditing && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleEdit}
              aria-label="Edit task"
            >
              Edit
            </Button>
          )}
          <motion.button
            onClick={() => onDelete(todo.id)}
            className="p-2 text-gray-500 hover:text-red-500 dark:text-gray-400 dark:hover:text-red-400 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            aria-label="Delete task"
          >
            <Trash2 size={18} />
          </motion.button>
        </div>
      </motion.div>
    </>
  );
};

export default SortableTodoItem;