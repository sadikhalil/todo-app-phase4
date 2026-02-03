import React from 'react';
import { TodoProvider } from '../contexts/TodoContext';
import TodoInput from '../components/TodoInput';
import TodoFilters from '../components/TodoFilters';
import SortableTodoList from '../components/SortableTodoList';
import ProgressBar from '../components/ProgressBar';
import Layout from '../components/Layout';
import { Toaster } from 'react-hot-toast';
import { useAuth } from '../contexts/AuthContext';

const TodoPage = () => {
  const { user } = useAuth();

  return (
    <TodoProvider>
      <Layout title="Modern Todo App" description="A modern, interactive todo application">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Hello, {user?.email?.split('@')[0]}! 👋
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            What would you like to accomplish today?
          </p>
        </div>

        <TodoInput />

        <div className="mt-8 w-full max-w-2xl">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Your Tasks</h2>
            <ProgressBar />
          </div>

          <TodoFilters />

          <div className="mt-4">
            <SortableTodoList />
          </div>
        </div>

        {/* Toast Notifications */}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 3000,
            style: {
              background: '#363636',
              color: '#fff',
            },
          }}
        />
      </Layout>
    </TodoProvider>
  );
};

export default TodoPage;