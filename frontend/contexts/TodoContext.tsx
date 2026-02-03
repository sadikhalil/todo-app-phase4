import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { Todo } from '../types/todo';
import { showToast } from '../components/Toast';
import { useAuth } from './AuthContext'; // Import AuthContext to get the token
import apiClient from '../lib/apiClient';

interface TodoState {
  todos: Todo[];
  filter: 'all' | 'active' | 'completed';
}

interface TodoContextType {
  state: TodoState;
  addTodo: (text: string, description?: string, dueDate?: Date, reminderDate?: Date, priority?: 'low' | 'medium' | 'high') => void;
  toggleTodo: (id: string) => void;
  deleteTodo: (id: string) => void;
  updateTodo: (id: string, text: string, description?: string, dueDate?: Date, reminderDate?: Date, priority?: 'low' | 'medium' | 'high') => void;
  clearCompleted: () => void;
  setFilter: (filter: 'all' | 'active' | 'completed') => void;
  reorderTodos: (activeId: string, overId: string) => void;
}

const TodoContext = createContext<TodoContextType | undefined>(undefined);

const todoReducer = (state: TodoState, action: any): TodoState => {
  switch (action.type) {
    case 'ADD_TODO':
      const newTodo: Todo = {
        id: Date.now().toString(),
        text: action.payload.text,
        description: action.payload.description,
        status: 'incomplete', // Changed from completed: false to status: 'incomplete'
        priority: action.payload.priority || 'medium',
        dueDate: action.payload.dueDate,
        reminderDate: action.payload.reminderDate,
        createdAt: new Date(),
        updatedAt: new Date(),
      };
      return {
        ...state,
        todos: [newTodo, ...state.todos],
      };

    case 'TOGGLE_TODO':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === action.payload.id
            ? { ...todo, status: todo.status === 'complete' ? 'incomplete' : 'complete', updatedAt: new Date() }
            : todo
        ),
      };

    case 'DELETE_TODO':
      return {
        ...state,
        todos: state.todos.filter(todo => todo.id !== action.payload.id),
      };

    case 'UPDATE_TODO':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === action.payload.id
            ? {
                ...todo,
                text: action.payload.text,
                description: action.payload.description ?? todo.description,
                priority: action.payload.priority ?? todo.priority,
                dueDate: action.payload.dueDate ?? todo.dueDate,
                reminderDate: action.payload.reminderDate ?? todo.reminderDate,
                updatedAt: new Date()
              }
            : todo
        ),
      };

    case 'CLEAR_COMPLETED':
      return {
        ...state,
        todos: state.todos.filter(todo => todo.status !== 'complete'),
      };

    case 'SET_FILTER':
      return {
        ...state,
        filter: action.payload.filter,
      };

    case 'REORDER_TODOS':
      const { activeId, overId } = action.payload;
      if (activeId === overId) return state;

      const oldIndex = state.todos.findIndex(item => item.id === activeId);
      const newIndex = state.todos.findIndex(item => item.id === overId);

      const newTodos = [...state.todos];
      const [movedItem] = newTodos.splice(oldIndex, 1);
      newTodos.splice(newIndex, 0, movedItem);

      return {
        ...state,
        todos: newTodos,
      };

    case 'LOAD_TODOS':
      return {
        ...state,
        todos: action.payload.todos || [],
      };

    default:
      return state;
  }
};

export const TodoProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Initialize from localStorage if available (only in browser)
  const initialState: TodoState = (() => {
    if (typeof window !== 'undefined') {
      try {
        const savedState = localStorage.getItem('todoAppState');
        if (savedState) {
          return JSON.parse(savedState);
        }
      } catch (e) {
        console.warn('Could not load todo state from localStorage', e);
      }
    }
    return {
      todos: [],
      filter: 'all',
    };
  })();

  const [state, dispatch] = useReducer(todoReducer, initialState);

  const { token } = useAuth(); // Get the authentication token

  // Load todos from backend API on initial render
  useEffect(() => {
    const fetchTodos = async () => {
      if (token) { // Only fetch if user is authenticated
        try {
          const data = await apiClient.getTasks();
          const fetchedTodos = data.tasks || [];

          // Convert dates from string to Date objects
          const todosWithDates = fetchedTodos.map((todo: any) => ({
            ...todo,
            createdAt: new Date(todo.created_at),
            updatedAt: new Date(todo.updated_at),
            dueDate: todo.due_date ? new Date(todo.due_date) : undefined,
            description: todo.description,
            priority: todo.priority,
            reminderDate: todo.reminder_date ? new Date(todo.reminder_date) : undefined,
          }));

          dispatch({ type: 'LOAD_TODOS', payload: { todos: todosWithDates } });
        } catch (e) {
          console.error('Failed to load todos from backend', e);
        }
      }
    };

    fetchTodos();
  }, [token]); // Fetch todos when token changes (on login/signup)

  const addTodo = async (text: string, description?: string, dueDate?: Date, reminderDate?: Date, priority?: 'low' | 'medium' | 'high') => {
    // Add locally first, then sync with backend if logged in
    dispatch({
      type: 'ADD_TODO',
      payload: {
        text,
        description,
        dueDate,
        reminderDate,
        priority: priority || 'medium'
      }
    });

    // Show success message
    showToast(`Added: ${text.substring(0, 30)}${text.length > 30 ? '...' : ''}`, 'success');

    // If user is logged in, also add to backend
    if (token) {
      try {
        await apiClient.createTask({
          title: text,
          description: description || undefined,
          due_date: dueDate ? dueDate.toISOString() : null,
          reminder_date: reminderDate ? reminderDate.toISOString() : null,
          priority: priority || 'medium',
          status: 'incomplete'
        });
      } catch (error) {
        console.error('Failed to sync todo to backend:', error);
        showToast('Failed to sync task to server', 'warning');
        // Keep the task in local state anyway
      }
    }
  };

  const toggleTodo = async (id: string) => {
    const todo = state.todos.find(t => t.id === id);
    if (!todo) return;

    // Toggle locally first
    dispatch({ type: 'TOGGLE_TODO', payload: { id } });
    const newStatus = todo.status === 'complete' ? 'incomplete' : 'complete';
    const action = todo.status === 'complete' ? 'marked as incomplete' : 'completed';
    showToast(`${action.charAt(0).toUpperCase() + action.slice(1)}: ${todo.text.substring(0, 30)}${todo.text.length > 30 ? '...' : ''}`, 'info');

    // If user is logged in, also sync to backend
    if (token) {
      try {
        await apiClient.updateTaskStatus(id, { status: newStatus });
      } catch (error) {
        console.error('Failed to sync toggle to backend:', error);
        showToast('Failed to sync status to server', 'warning');
        // Status is already toggled locally, which is fine
      }
    }
  };

  const deleteTodo = async (id: string) => {
    const todo = state.todos.find(t => t.id === id);
    if (!todo) return;

    // Delete locally first
    dispatch({ type: 'DELETE_TODO', payload: { id } });
    showToast(`Deleted: ${todo.text.substring(0, 30)}${todo.text.length > 30 ? '...' : ''}`, 'warning');

    // If user is logged in, also delete from backend
    if (token) {
      try {
        await apiClient.deleteTask(id);
      } catch (error) {
        console.error('Failed to sync deletion to backend:', error);
        showToast('Failed to sync deletion to server', 'warning');
        // Task is already deleted locally, which is fine
      }
    }
  };

  const updateTodo = async (id: string, text: string, description?: string, dueDate?: Date, reminderDate?: Date, priority?: 'low' | 'medium' | 'high') => {
    const oldTodo = state.todos.find(t => t.id === id);
    if (!oldTodo) return;

    // Update locally first
    dispatch({
      type: 'UPDATE_TODO',
      payload: {
        id,
        text,
        description,
        dueDate,
        reminderDate,
        priority
      }
    });
    showToast(`Updated: ${text.substring(0, 30)}${text.length > 30 ? '...' : ''}`, 'success');

    // If user is logged in, also update backend
    if (token) {
      try {
        await apiClient.updateTask(id, {
          title: text,
          description: description ?? oldTodo.description,
          due_date: dueDate ? dueDate.toISOString() : null,
          reminder_date: reminderDate ? reminderDate.toISOString() : null,
          priority: priority ?? oldTodo.priority ?? 'medium'
        });
      } catch (error) {
        console.error('Failed to sync update to backend:', error);
        showToast('Failed to sync update to server', 'warning');
        // Keep the local update anyway
      }
    }
  };

  const clearCompleted = async () => {
    if (token) { // Only show warning if logged in and trying to clear
      try {
        // Get completed tasks to delete
        const completedTodos = state.todos.filter(todo => todo.status === 'complete');

        // Delete each completed task individually (since backend doesn't have a bulk delete endpoint)
        const promises = completedTodos.map(todo =>
          apiClient.deleteTask(todo.id)
        );

        await Promise.all(promises);

        dispatch({ type: 'CLEAR_COMPLETED' });
        showToast(`Cleared ${completedTodos.length} completed tasks`, 'info');
      } catch (error) {
        console.error('Failed to clear completed todos:', error);
        showToast('Failed to clear completed tasks', 'error');
      }
    } else {
      // Clear locally without backend sync
      const completedCount = state.todos.filter(todo => todo.status === 'complete').length;
      if (completedCount > 0) {
        dispatch({ type: 'CLEAR_COMPLETED' });
        showToast(`Cleared ${completedCount} completed tasks`, 'info');
      }
    }
  };

  const setFilter = (filter: 'all' | 'active' | 'completed') => {
    dispatch({ type: 'SET_FILTER', payload: { filter } });
  };

  const reorderTodos = (activeId: string, overId: string) => {
    // For now, just reorder locally since backend doesn't have a reorder endpoint
    // In a real implementation, we would call an API endpoint to persist the order
    dispatch({ type: 'REORDER_TODOS', payload: { activeId, overId } });
    showToast('Task reordered', 'info');
  };

  const value = {
    state,
    addTodo,
    toggleTodo,
    deleteTodo,
    updateTodo,
    clearCompleted,
    setFilter,
    reorderTodos,
  };

  // Effect to save state to localStorage whenever it changes (only in browser)
  useEffect(() => {
    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem('todoAppState', JSON.stringify(state));
      } catch (e) {
        console.warn('Could not save todo state to localStorage', e);
      }
    }
  }, [state]);

  return <TodoContext.Provider value={value}>{children}</TodoContext.Provider>;
};

export const useTodo = (): TodoContextType => {
  const context = useContext(TodoContext);
  if (!context) {
    throw new Error('useTodo must be used within a TodoProvider');
  }
  return context;
};