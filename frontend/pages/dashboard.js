import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '../contexts/AuthContext';
import { useTodo } from '../contexts/TodoContext';
import { format } from 'date-fns';
import FloatingChatButton from '../components/FloatingChatButton';
import TodoInput from '../components/TodoInput';
import TodoList from '../components/TodoList';
import TodoFilters from '../components/TodoFilters';
import SortableTodoList from '../components/SortableTodoList';
import ProgressBar from '../components/ProgressBar';

const DashboardPage = () => {
  const [selectedFilter, setSelectedFilter] = useState('all'); // all, incomplete, complete
  const [sortBy, setSortBy] = useState('created_at'); // created_at, updated_at, title, priority
  const [sortOrder, setSortOrder] = useState('desc'); // asc, desc
  const [currentPage, setCurrentPage] = useState(0);
  const [limit] = useState(10);

  const { user, logout } = useAuth();
  const { state, addTodo, updateTodo, deleteTodo, toggleTodo } = useTodo();
  const tasks = state.todos;

  useEffect(() => {
    // Tasks are managed by TodoContext, no need to fetch separately
  }, []);

  // Apply filters and sorting to tasks
  const filteredTasks = tasks.filter(task => {
    if (selectedFilter === 'complete') return task.status === 'complete';
    if (selectedFilter === 'incomplete') return task.status === 'incomplete';
    return true; // 'all'
  });

  // Calculate stats
  const stats = {
    total: tasks.length,
    completed: tasks.filter(t => t.status === 'complete').length,
    incomplete: tasks.filter(t => t.status === 'incomplete').length,
    by_priority: {
      high: tasks.filter(t => t.priority === 'high').length,
      medium: tasks.filter(t => t.priority === 'medium').length,
      low: tasks.filter(t => t.priority === 'low').length
    }
  };

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  // Get priority badge class
  const getPriorityClass = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  // Format date for display
  const formatDate = (dateString) => {
    try {
      return format(new Date(dateString), 'MMM dd, yyyy');
    } catch {
      return 'N/A';
    }
  };

  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="min-h-screen bg-white dark:bg-navy-blue text-navy-blue dark:text-white flex">
      {/* Mobile menu button */}
      <button
        onClick={toggleSidebar}
        className="fixed top-4 left-4 z-50 p-2 rounded-md text-white bg-navy-blue lg:hidden"
        aria-label="Toggle menu"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      {/* Mobile backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={toggleSidebar}
        ></div>
      )}

      {/* Sidebar */}
      <aside
        id="sidebar"
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-navy-blue text-white shadow-lg flex flex-col transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:z-40 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* User Profile Section */}
        <div className="p-6 border-b border-gray-700">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-peach rounded-full flex items-center justify-center text-navy-blue font-bold">
              {user?.email?.charAt(0)?.toUpperCase() || 'U'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{user?.email || 'User'}</p>
              <p className="text-xs text-gray-300 truncate">Member</p>
            </div>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 py-4">
          <ul className="space-y-1 px-3">
            <li>
              <Link
                href="/dashboard"
                className="flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium bg-peach text-navy-blue"
              >
                <span className="text-lg">📊</span>
                <span>Dashboard</span>
              </Link>
            </li>
            <li>
              <Link
                href="/todo"
                className="flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white"
              >
                <span className="text-lg">✅</span>
                <span>Tasks</span>
              </Link>
            </li>
            <li>
              <button
                onClick={() => {
                  // Open the chat panel by triggering the floating chat button
                  const chatButton = document.querySelector('.floating-chat-button');
                  if (chatButton) {
                    chatButton.click();
                  }
                }}
                className="flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white w-full text-left"
              >
                <span className="text-lg">💬</span>
                <span>Chat</span>
              </button>
            </li>
            {/* Removed Settings link as requested */}
          </ul>
        </nav>

        {/* Logout Button */}
        <div className="p-4 border-t border-gray-700">
          <button
            onClick={handleLogout}
            className="w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white"
          >
            <span className="text-lg">🚪</span>
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* Mobile overlay */}
      <div className="fixed inset-0 z-30 bg-black bg-opacity-50 lg:hidden hidden" id="mobile-menu-overlay"></div>

      {/* Main Content */}
      <main className={`flex-1 flex flex-col transition-all duration-300 ${sidebarOpen ? 'lg:ml-64' : 'ml-0 lg:ml-64'}`}>
        {/* Top Header */}
        <header className="bg-white dark:bg-navy-blue shadow-sm border-b border-gray-200 dark:border-gray-700 p-4 sm:p-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <h1 className="text-xl sm:text-2xl font-bold text-navy-blue dark:text-white">Todo Dashboard</h1>
            <div className="flex items-center space-x-4 w-full sm:w-auto justify-between sm:justify-end">
              <span className="text-navy-blue dark:text-white font-medium text-sm sm:text-base">Welcome, {user?.email}</span>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <div className="flex-1 p-4 sm:p-6">
          {/* Stats Summary */}
          <div className="grid grid-cols-1 gap-4 sm:gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-6 sm:mb-8">
            <div className="bg-white dark:bg-navy-blue overflow-hidden shadow-lg rounded-xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-transform duration-200 hover:scale-[1.02]">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-navy-blue rounded-lg p-2 sm:p-3">
                  <svg className="h-5 w-5 sm:h-6 sm:w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <div className="ml-3 sm:ml-4 w-0 flex-1">
                  <dl>
                    <dt className="text-xs sm:text-sm font-medium text-gray-500 dark:text-gray-400 truncate">Total Tasks</dt>
                    <dd className="flex items-baseline">
                      <div className="text-xl sm:text-3xl font-bold text-navy-blue dark:text-white">{stats.total}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-navy-blue overflow-hidden shadow-lg rounded-xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-transform duration-200 hover:scale-[1.02]">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-green-500 rounded-lg p-2 sm:p-3">
                  <svg className="h-5 w-5 sm:h-6 sm:w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-3 sm:ml-4 w-0 flex-1">
                  <dl>
                    <dt className="text-xs sm:text-sm font-medium text-gray-500 dark:text-gray-400 truncate">Completed</dt>
                    <dd className="flex items-baseline">
                      <div className="text-xl sm:text-3xl font-bold text-navy-blue dark:text-white">{stats.completed}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-navy-blue overflow-hidden shadow-lg rounded-xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-transform duration-200 hover:scale-[1.02]">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-orange rounded-lg p-2 sm:p-3">
                  <svg className="h-5 w-5 sm:h-6 sm:w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-3 sm:ml-4 w-0 flex-1">
                  <dl>
                    <dt className="text-xs sm:text-sm font-medium text-gray-500 dark:text-gray-400 truncate">Incomplete</dt>
                    <dd className="flex items-baseline">
                      <div className="text-xl sm:text-3xl font-bold text-navy-blue dark:text-white">{stats.incomplete}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-navy-blue overflow-hidden shadow-lg rounded-xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-transform duration-200 hover:scale-[1.02]">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-purple-500 rounded-lg p-2 sm:p-3">
                  <svg className="h-5 w-5 sm:h-6 sm:w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                  </svg>
                </div>
                <div className="ml-3 sm:ml-4 w-0 flex-1">
                  <dl>
                    <dt className="text-xs sm:text-sm font-medium text-gray-500 dark:text-gray-400 truncate">High Priority</dt>
                    <dd className="flex items-baseline">
                      <div className="text-xl sm:text-3xl font-bold text-navy-blue dark:text-white">{stats.by_priority.high}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 gap-6">
            {/* Todo Input Section - Full width on mobile, side by side on larger screens */}
            <div className="bg-white dark:bg-navy-blue shadow-lg rounded-xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6">
              <h2 className="text-lg sm:text-xl font-semibold text-navy-blue dark:text-white mb-4">Add New Task</h2>
              <TodoInput />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Filters Section */}
              <div className="lg:col-span-1">
                <div className="bg-white dark:bg-navy-blue shadow-lg rounded-xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6">
                  <h3 className="text-base sm:text-lg font-medium text-navy-blue dark:text-white mb-4">Filters</h3>
                  <TodoFilters />
                </div>
              </div>

              {/* Task List Section */}
              <div className="lg:col-span-2">
                <div className="bg-white dark:bg-navy-blue shadow-lg rounded-xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6">
                  <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                    <h2 className="text-lg sm:text-xl font-semibold text-navy-blue dark:text-white">Your Tasks</h2>
                    <div className="w-full sm:w-auto">
                      <ProgressBar />
                    </div>
                  </div>

                  <SortableTodoList />
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Floating Chat Button */}
      <FloatingChatButton
        userId={user?.id}
        userToken={typeof window !== 'undefined' ? localStorage.getItem('access_token') : null}
      />
    </div>
  );
};

export default DashboardPage;