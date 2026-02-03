import React from 'react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from '@dnd-kit/core';
import {
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { useTodo } from '../contexts/TodoContext';
import SortableTodoItem from './SortableTodoItem';
import { AnimatePresence } from 'framer-motion';

const SortableTodoList: React.FC = () => {
  const { state, toggleTodo, deleteTodo, updateTodo, reorderTodos } = useTodo();

  // Filter todos based on the current filter
  const filteredTodos = state.todos.filter(todo => {
    if (state.filter === 'active') return todo.status !== 'complete';
    if (state.filter === 'completed') return todo.status === 'complete';
    return true; // 'all'
  });

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      // Find the active and over items in the filtered list
      const activeIndex = filteredTodos.findIndex(todo => todo.id === active.id);
      const overIndex = filteredTodos.findIndex(todo => todo.id === over.id);

      if (activeIndex !== -1 && overIndex !== -1) {
        // Use the reorderTodos function from context to update the order
        reorderTodos(String(active.id), String(over.id));
      }
    }
  };

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      <div className="w-full max-w-2xl">
        <SortableContext
          items={filteredTodos.map(todo => todo.id)}
          strategy={verticalListSortingStrategy}
        >
          <AnimatePresence>
            {filteredTodos.length > 0 ? (
              <ul className="space-y-3">
                {filteredTodos.map(todo => (
                  <SortableTodoItem
                    key={todo.id}
                    todo={todo}
                    onToggle={toggleTodo}
                    onDelete={deleteTodo}
                    onEdit={updateTodo}
                  />
                ))}
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
        </SortableContext>
      </div>
    </DndContext>
  );
};

export default SortableTodoList;