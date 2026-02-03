import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '../contexts/AuthContext';
import { useTodo } from '../contexts/TodoContext';
import Layout from '../components/Layout';
import { format } from 'date-fns';

const DashboardPage = () => {
  const [showCreateForm, setShowCreateForm] = useState(false);
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

  // Sort tasks
  const sortedTasks = [...filteredTasks].sort((a, b) => {
    let aValue, bValue;

    switch (sortBy) {
      case 'title':
        aValue = a.text.toLowerCase();
        bValue = b.text.toLowerCase();
        break;
      case 'priority':
        // High > Medium > Low
        const priorityOrder = { 'high': 3, 'medium': 2, 'low': 1 };
        return sortOrder === 'desc' ? priorityOrder[b.priority] - priorityOrder[a.priority] : priorityOrder[a.priority] - priorityOrder[b.priority];
      case 'created_at':
        aValue = new Date(a.createdAt).getTime();
        bValue = new Date(b.createdAt).getTime();
        break;
      case 'updated_at':
        aValue = new Date(a.updatedAt).getTime();
        bValue = new Date(b.updatedAt).getTime();
        break;
      default:
        aValue = new Date(a.createdAt).getTime();
        bValue = new Date(b.createdAt).getTime();
    }

    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return sortOrder === 'desc' ? bValue.localeCompare(aValue) : aValue.localeCompare(bValue);
    }
    return sortOrder === 'desc' ? bValue - aValue : aValue - bValue;
  });

  // Apply pagination
  const paginatedTasks = sortedTasks.slice(currentPage * limit, (currentPage + 1) * limit);

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

  const createTask = async (taskData) => {
    // Use the context function to add the task
    addTodo(taskData.title, taskData.description, undefined, undefined, taskData.priority);

    // Reset form and hide it
    setShowCreateForm(false);
  };

  const updateTask = async (taskId, taskData) => {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    // Use the context function to update the task
    updateTodo(
      taskId,
      taskData.title || task.text,
      taskData.description || task.description,
      task.dueDate,
      task.reminderDate,
      taskData.priority || task.priority
    );
  };

  const toggleTaskCompletion = async (taskId) => {
    // Use the context function to toggle the task
    toggleTodo(taskId);
  };

  const deleteTask = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task? This action cannot be undone!')) {
      // Use the context function to delete the task
      deleteTodo(taskId);
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

  return (
    <Layout title="Todo Dashboard">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Todo Dashboard</h1>
          <div className="flex items-center space-x-4">
            <Link
              href="/chat"
              className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              AI Chat
            </Link>
            <span className="text-gray-700">Welcome, {user?.email}</span>
            <button
              onClick={handleLogout}
              className="ml-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {/* Stats Summary */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                  <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Total Tasks</dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">{stats.total}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                  <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Completed</dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">{stats.completed}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-yellow-500 rounded-md p-3">
                  <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Incomplete</dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">{stats.incomplete}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-purple-500 rounded-md p-3">
                  <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                  </svg>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">High Priority</dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">{stats.by_priority.high}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Controls */}
        <div className="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
          <div className="flex space-x-2">
            <button
              onClick={() => setShowCreateForm(!showCreateForm)}
              className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              {showCreateForm ? 'Cancel' : 'Add Task'}
            </button>

            <select
              value={selectedFilter}
              onChange={(e) => setSelectedFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="all">All Tasks</option>
              <option value="incomplete">Incomplete</option>
              <option value="complete">Complete</option>
            </select>

            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="created_at">Created At</option>
              <option value="updated_at">Updated At</option>
              <option value="title">Title</option>
              <option value="priority">Priority</option>
            </select>

            <select
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="asc">Ascending</option>
              <option value="desc">Descending</option>
            </select>
          </div>
        </div>

        {/* Task Creation Form */}
        {showCreateForm && (
          <div className="mb-6">
            <div className="bg-white shadow overflow-hidden sm:rounded-md">
              <div className="p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Add New Task</h2>

                <form onSubmit={(e) => {
                  e.preventDefault();
                  const formData = new FormData(e.target);
                  createTask({
                    title: formData.get('title'),
                    description: formData.get('description'),
                    priority: formData.get('priority')
                  });
                }}>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                        Task Title *
                      </label>
                      <input
                        id="title"
                        name="title"
                        type="text"
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                        placeholder="What needs to be done?"
                      />
                    </div>

                    <div>
                      <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
                        Priority
                      </label>
                      <select
                        id="priority"
                        name="priority"
                        defaultValue="medium"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      >
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                      </select>
                    </div>
                  </div>

                  <div className="mb-4">
                    <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                      Description
                    </label>
                    <textarea
                      id="description"
                      name="description"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      placeholder="Add details..."
                      rows="2"
                    />
                  </div>

                  <div className="flex justify-end">
                    <button
                      type="submit"
                      className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      Add Task
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        )}

        {/* Task List */}
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          {paginatedTasks.length === 0 ? (
            <div className="text-center py-12">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
              <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
              <div className="mt-6">
                <button
                  onClick={() => setShowCreateForm(true)}
                  className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Add Task
                </button>
              </div>
            </div>
          ) : (
            <ul className="divide-y divide-gray-200">
              {paginatedTasks.map((task) => (
                <li key={task.id} className="hover:bg-gray-50">
                  <div className="px-4 py-4 sm:px-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          checked={task.status === 'complete'}
                          onChange={() => toggleTaskCompletion(task.id)}
                          className="h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500"
                        />
                        <div className="ml-3 flex items-center">
                          <p className={`text-sm font-medium ${
                            task.status === 'complete'
                              ? 'text-gray-500 line-through'
                              : 'text-gray-900'
                          }`}>
                            {task.text}
                          </p>
                          <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityClass(task.priority)}`}>
                            {task.priority}
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm text-gray-500">
                          Created: {formatDate(task.createdAt)}
                        </span>
                        <button
                          onClick={() => {
                            // Set up edit form with task data
                            document.getElementById(`edit-form-${task.id}`).classList.remove('hidden');
                            document.getElementById(`task-display-${task.id}`).classList.add('hidden');
                          }}
                          className="inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => deleteTask(task.id)}
                          className="inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                    {task.description && (
                      <div className="mt-2 sm:flex sm:justify-between">
                        <div className="sm:flex">
                          <p className="flex items-center text-sm text-gray-600">
                            {task.description}
                          </p>
                        </div>
                      </div>
                    )}

                    {/* Edit Form - Initially hidden */}
                    <div id={`edit-form-${task.id}`} className="hidden mt-4 p-4 bg-gray-50 rounded-md">
                      <form onSubmit={(e) => {
                        e.preventDefault();
                        const formData = new FormData(e.target);
                        updateTask(task.id, {
                          title: formData.get('title'),
                          description: formData.get('description'),
                          priority: formData.get('priority')
                        });
                        // Hide edit form and show display
                        document.getElementById(`edit-form-${task.id}`).classList.add('hidden');
                        document.getElementById(`task-display-${task.id}`).classList.remove('hidden');
                      }}>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                          <div>
                            <label htmlFor={`edit-title-${task.id}`} className="block text-sm font-medium text-gray-700 mb-1">
                              Task Title
                            </label>
                            <input
                              id={`edit-title-${task.id}`}
                              name="title"
                              type="text"
                              defaultValue={task.text}
                              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                            />
                          </div>

                          <div>
                            <label htmlFor={`edit-priority-${task.id}`} className="block text-sm font-medium text-gray-700 mb-1">
                              Priority
                            </label>
                            <select
                              id={`edit-priority-${task.id}`}
                              name="priority"
                              defaultValue={task.priority}
                              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                            >
                              <option value="low">Low</option>
                              <option value="medium">Medium</option>
                              <option value="high">High</option>
                            </select>
                          </div>
                        </div>

                        <div className="mb-4">
                          <label htmlFor={`edit-description-${task.id}`} className="block text-sm font-medium text-gray-700 mb-1">
                            Description
                          </label>
                          <textarea
                            id={`edit-description-${task.id}`}
                            name="description"
                            defaultValue={task.description || ''}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                            rows="2"
                          />
                        </div>

                        <div className="flex justify-end space-x-2">
                          <button
                            type="button"
                            onClick={() => {
                              document.getElementById(`edit-form-${task.id}`).classList.add('hidden');
                              document.getElementById(`task-display-${task.id}`).classList.remove('hidden');
                            }}
                            className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                          >
                            Cancel
                          </button>
                          <button
                            type="submit"
                            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                          >
                            Save
                          </button>
                        </div>
                      </form>
                    </div>

                    {/* Task Display Container - Initially shown */}
                    <div id={`task-display-${task.id}`} className="hidden">
                      {/* This div exists to toggle visibility */}
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Pagination */}
        {sortedTasks.length > limit && (
          <div className="mt-6 flex justify-center">
            <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
              <button
                onClick={() => setCurrentPage(Math.max(0, currentPage - 1))}
                disabled={currentPage === 0}
                className={`relative inline-flex items-center px-4 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium ${
                  currentPage === 0
                    ? 'text-gray-400 cursor-not-allowed'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                Previous
              </button>

              <span className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                {currentPage + 1}
              </span>

              <button
                onClick={() => setCurrentPage(currentPage + 1)}
                disabled={(currentPage + 1) * limit >= sortedTasks.length}
                className={`relative inline-flex items-center px-4 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium ${
                  (currentPage + 1) * limit >= sortedTasks.length
                    ? 'text-gray-400 cursor-not-allowed'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                Next
              </button>
            </nav>
          </div>
        )}
      </main>
    </Layout>
  );
};

export default DashboardPage;
