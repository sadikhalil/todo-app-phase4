import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Trash2, CheckCircle, Circle } from 'lucide-react';
import { Todo } from '../types/todo';
import Button from './ui/Button';
import ConfettiEffect from './ConfettiEffect';

interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
  onEdit: (id: string, text: string, description?: string, dueDate?: Date, reminderDate?: Date, priority?: 'low' | 'medium' | 'high') => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggle, onDelete, onEdit }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(todo.text);
  const [editDescription, setEditDescription] = useState(todo.description || '');
  const [editDueDate, setEditDueDate] = useState(todo.dueDate ? new Date(todo.dueDate).toISOString().split('T')[0] : '');
  const [editReminderDate, setEditReminderDate] = useState(todo.reminderDate ? new Date(todo.reminderDate).toISOString().slice(0, 16) : '');
  const [editPriority, setEditPriority] = useState(todo.priority || 'medium');
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

  const handleEdit = () => {
    setIsEditing(!isEditing);
  };

  const handleCancelEdit = () => {
    setEditText(todo.text);
    setEditDescription(todo.description || '');
    setEditDueDate(todo.dueDate ? new Date(todo.dueDate).toISOString().split('T')[0] : '');
    setEditReminderDate(todo.reminderDate ? new Date(todo.reminderDate).toISOString().slice(0, 16) : '');
    setEditPriority(todo.priority || 'medium');
    setIsEditing(false);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onEdit(todo.id, editText, editDescription || undefined, editDueDate ? new Date(editDueDate) : undefined, editReminderDate ? new Date(editReminderDate) : undefined, editPriority);
    setIsEditing(false);
  };

  return (
    <>
      {showConfetti && <ConfettiEffect isActive={true} />}
      <motion.li
        layout
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: -20, height: 0, scale: 0.95 }}
        transition={{ duration: 0.3, ease: "easeOut" }}
        className="relative p-5 bg-white dark:bg-navy-blue rounded-xl shadow-md hover:shadow-lg transition-all duration-200 border border-gray-200 dark:border-gray-700 hover:border-orange dark:hover:border-orange"
      >
        <div className="flex flex-col space-y-3 flex-1 min-w-0">
          <div className="flex items-start space-x-3">
            <motion.button
              onClick={() => onToggle(todo.id)}
              className="flex-shrink-0 mt-1"
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
              <form onSubmit={handleSubmit} className="flex-1 min-w-0 space-y-3">
                <div className="space-y-3">
                  <input
                    type="text"
                    value={editText}
                    onChange={(e) => setEditText(e.target.value)}
                    className="w-full bg-transparent border-b border-orange focus:outline-none focus:border-navy-blue pb-2 text-lg font-medium"
                    autoFocus
                  />

                  <textarea
                    value={editDescription}
                    onChange={(e) => setEditDescription(e.target.value)}
                    placeholder="Add description..."
                    className="w-full bg-transparent border-b border-orange focus:outline-none focus:border-navy-blue pb-2 text-sm"
                    rows={2}
                  />

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-2">
                    <div>
                      <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">Priority</label>
                      <select
                        value={editPriority}
                        onChange={(e) => setEditPriority(e.target.value as 'low' | 'medium' | 'high')}
                        className="w-full bg-transparent border-b border-orange focus:outline-none focus:border-navy-blue text-sm"
                      >
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">Due Date</label>
                      <input
                        type="date"
                        value={editDueDate}
                        onChange={(e) => setEditDueDate(e.target.value)}
                        className="w-full bg-transparent border-b border-orange focus:outline-none focus:border-navy-blue text-sm"
                      />
                    </div>

                    <div>
                      <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">Reminder</label>
                      <input
                        type="datetime-local"
                        value={editReminderDate}
                        onChange={(e) => setEditReminderDate(e.target.value)}
                        className="w-full bg-transparent border-b border-orange focus:outline-none focus:border-navy-blue text-sm"
                      />
                    </div>
                  </div>
                </div>

                <div className="flex space-x-2 mt-3">
                  <Button size="sm" type="submit">Save</Button>
                  <Button size="sm" variant="ghost" onClick={handleCancelEdit}>Cancel</Button>
                </div>
              </form>
            ) : (
              <div className="flex-1 min-w-0">
                <motion.div
                  className={`font-medium ${todo.status === 'complete' ? 'line-through text-gray-500 dark:text-gray-500' : 'text-navy-blue dark:text-white'}`}
                  animate={{
                    textDecoration: todo.status === 'complete' ? 'line-through' : 'none',
                    color: todo.status === 'complete' ? '#9CA3AF' : '#1F2937'
                  }}
                  transition={{ duration: 0.3 }}
                >
                  {todo.text}
                </motion.div>

                {todo.description && (
                  <div className="text-sm text-navy-blue dark:text-gray-300 mt-2">
                    {todo.description}
                  </div>
                )}

                <div className="flex flex-wrap items-center gap-2 mt-3">
                  {todo.dueDate && (
                    <div className="flex items-center text-xs px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-md text-navy-blue dark:text-gray-300">
                      <span className="mr-1">📅</span>
                      {new Date(todo.dueDate).toLocaleDateString()}
                    </div>
                  )}
                  {todo.priority && (
                    <div className={`text-xs px-2 py-1 rounded-md ${
                      todo.priority === 'high' ? 'bg-orange text-navy-blue' :
                      todo.priority === 'medium' ? 'bg-peach text-navy-blue' :
                      'bg-navy-blue text-white'
                    }`}>
                      {todo.priority} priority
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          <div className="flex justify-end">
            <div className="flex items-center space-x-2">
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
                onClick={async () => {
                  if (window.confirm('Are you sure you want to delete this task? This action cannot be undone!')) {
                    onDelete(todo.id);
                  }
                }}
                className="p-2 text-navy-blue hover:text-red-500 dark:text-white dark:hover:text-red-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                aria-label="Delete task"
              >
                <Trash2 size={16} />
              </motion.button>
            </div>
          </div>
        </div>
      </motion.li>
    </>
  );
};

export default TodoItem;