"""Frontend Agent - Creates a beautiful and interactive Next.js web interface for the multi-user Todo application.

Role:
Responsible for building the frontend web application with Next.js.

Responsibilities:
- Create user interface for authentication and task management
- Communicate with backend APIs
- Manage client-side authentication state
- Implement beautiful and responsive UI

Skills:
- Frontend development (Next.js)
- HTTP API integration
- State management
- Form handling
- Responsive design
- Beautiful UI/UX

Requirements:
- Login page with beautiful design
- Signup page with beautiful design
- Todo dashboard page with beautiful design
- Ability to add, update, delete, and complete tasks
- Send authentication token with every API request
- Responsive and mobile-friendly design
- Interactive and smooth user experience

Inputs:
- User actions
- API responses from backend

Outputs:
- Frontend pages and components
- API client logic
- Auth state management
- Beautiful UI components

Constraints:
- No AI chat interface
- No server-side business logic
- No direct database access

Agent Coordination Rules:
- Auth-agent defines security rules used by backend-agent
- Database-agent provides models used by backend-agent
- Backend-agent exposes APIs consumed by frontend-agent
- Frontend-agent must not bypass backend or database logic
"""

import os
import json
from typing import Dict, Any, Optional


class NextJSComponentGenerator:
    """Generates Next.js components for the beautiful UI."""

    def __init__(self):
        self.components_dir = "components"
        self.pages_dir = "pages"

    def generate_layout_component(self):
        """Generate the main layout component."""
        layout_content = '''import React from 'react';
import Head from 'next/head';
import Header from './Header';

const Layout = ({ children, title = "Todo App" }) => {
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <Header />
        <main className="container mx-auto px-4 py-8 max-w-4xl">
          {children}
        </main>
      </div>
    </>
  );
};

export default Layout;
'''
        return layout_content

    def generate_header_component(self):
        """Generate the header component."""
        header_content = '''import React, { useContext } from 'react';
import Link from 'next/link';
import { AuthContext } from '../contexts/AuthContext';

const Header = () => {
  const { user, logout, isAuthenticated } = useContext(AuthContext);

  const handleLogout = () => {
    logout();
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4 max-w-4xl flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-indigo-600 hover:text-indigo-700 transition-colors">
          Todo App
        </Link>

        <nav className="flex items-center space-x-6">
          {isAuthenticated ? (
            <>
              <span className="text-gray-700">Welcome, {user?.email}</span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link href="/login" className="text-gray-700 hover:text-indigo-600 transition-colors">
                Login
              </Link>
              <Link href="/signup" className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
                Sign Up
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;
'''
        return header_content

    def generate_auth_context(self):
        """Generate the authentication context."""
        auth_context_content = '''import React, { createContext, useState, useEffect } from 'react';
import { useRouter } from 'next/router';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in on initial load
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (data.success) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        setToken(data.token);
        setUser(data.user);
        router.push('/dashboard');
        return { success: true, message: data.message };
      } else {
        return { success: false, message: data.message };
      }
    } catch (error) {
      return { success: false, message: 'An error occurred during login' };
    }
  };

  const signup = async (email, password) => {
    try {
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (data.success) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        setToken(data.token);
        setUser(data.user);
        router.push('/dashboard');
        return { success: true, message: data.message };
      } else {
        return { success: false, message: data.message };
      }
    } catch (error) {
      return { success: false, message: 'An error occurred during signup' };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
    router.push('/');
  };

  const value = {
    user,
    token,
    login,
    signup,
    logout,
    isAuthenticated: !!token,
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
'''
        return auth_context_content

    def generate_login_page(self):
        """Generate the login page."""
        login_page_content = '''import React, { useContext, useState } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login } = useContext(AuthContext);
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await login(email, password);

    if (!result.success) {
      setError(result.message);
      setLoading(false);
    }
  };

  return (
    <Layout title="Login - Todo App">
      <div className="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl p-8">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">Welcome Back</h1>

        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="your@email.com"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3 px-4 rounded-lg text-white font-medium ${
              loading ? 'bg-indigo-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'
            } transition-colors`}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Don't have an account?{' '}
            <a href="/signup" className="text-indigo-600 hover:text-indigo-800 font-medium">
              Sign up
            </a>
          </p>
        </div>
      </div>
    </Layout>
  );
};

export default LoginPage;
'''
        return login_page_content

    def generate_signup_page(self):
        """Generate the signup page."""
        signup_page_content = '''import React, { useContext, useState } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';

const SignupPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { signup } = useContext(AuthContext);
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    const result = await signup(email, password);

    if (!result.success) {
      setError(result.message);
      setLoading(false);
    }
  };

  return (
    <Layout title="Sign Up - Todo App">
      <div className="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl p-8">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">Create Account</h1>

        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="your@email.com"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="••••••••"
            />
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3 px-4 rounded-lg text-white font-medium ${
              loading ? 'bg-indigo-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'
            } transition-colors`}
          >
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Already have an account?{' '}
            <a href="/login" className="text-indigo-600 hover:text-indigo-800 font-medium">
              Sign in
            </a>
          </p>
        </div>
      </div>
    </Layout>
  );
};

export default SignupPage;
'''
        return signup_page_content

    def generate_dashboard_page(self):
        """Generate the dashboard page with task management."""
        dashboard_page_content = '''import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import Layout from '../components/Layout';

const DashboardPage = () => {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [editingTask, setEditingTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const { token, isAuthenticated } = useContext(AuthContext);

  useEffect(() => {
    if (isAuthenticated) {
      fetchTasks();
    }
  }, [isAuthenticated]);

  const fetchTasks = async () => {
    try {
      const response = await fetch('/api/tasks', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (data.success) {
        setTasks(data.data || []);
      } else {
        setError(data.message || 'Failed to fetch tasks');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/api/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: newTask.title,
          description: newTask.description,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setNewTask({ title: '', description: '' });
        fetchTasks(); // Refresh tasks
      } else {
        setError(data.message || 'Failed to create task');
      }
    } catch (err) {
      setError('Network error occurred');
    }
  };

  const updateTask = async (taskId) => {
    try {
      const response = await fetch(`/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: editingTask.title,
          description: editingTask.description,
          completed: editingTask.completed,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setEditingTask(null);
        fetchTasks(); // Refresh tasks
      } else {
        setError(data.message || 'Failed to update task');
      }
    } catch (err) {
      setError('Network error occurred');
    }
  };

  const toggleTaskCompletion = async (taskId, currentStatus) => {
    try {
      const response = await fetch(`/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          completed: !currentStatus,
        }),
      });

      const data = await response.json();

      if (data.success) {
        fetchTasks(); // Refresh tasks
      } else {
        setError(data.message || 'Failed to update task');
      }
    } catch (err) {
      setError('Network error occurred');
    }
  };

  const deleteTask = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        const response = await fetch(`/api/tasks/${taskId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        const data = await response.json();

        if (data.success) {
          fetchTasks(); // Refresh tasks
        } else {
          setError(data.message || 'Failed to delete task');
        }
      } catch (err) {
        setError('Network error occurred');
      }
    }
  };

  if (loading) {
    return (
      <Layout title="Loading - Todo App">
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Dashboard - Todo App">
      <div className="bg-white rounded-xl shadow-md p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Your Tasks</h1>

        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Add Task Form */}
        <form onSubmit={createTask} className="mb-8 p-4 bg-gray-50 rounded-lg">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Add New Task</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                Title *
              </label>
              <input
                id="title"
                type="text"
                required
                value={newTask.title}
                onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="What needs to be done?"
              />
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                id="description"
                value={newTask.description}
                onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Add details..."
                rows="2"
              />
            </div>
          </div>
          <button
            type="submit"
            className="mt-4 px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Add Task
          </button>
        </form>

        {/* Tasks List */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Your Tasks ({tasks.length})</h2>

          {tasks.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p>No tasks yet. Add your first task above!</p>
            </div>
          ) : (
            <div className="space-y-3">
              {tasks.map((task) => (
                <div
                  key={task.id}
                  className={`p-4 rounded-lg border ${
                    task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'
                  }`}
                >
                  {editingTask && editingTask.id === task.id ? (
                    // Edit mode
                    <div className="space-y-3">
                      <input
                        type="text"
                        value={editingTask.title}
                        onChange={(e) => setEditingTask({ ...editingTask, title: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 mb-2"
                      />
                      <textarea
                        value={editingTask.description}
                        onChange={(e) => setEditingTask({ ...editingTask, description: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 mb-2"
                        rows="2"
                      />
                      <div className="flex space-x-2">
                        <button
                          onClick={() => updateTask(task.id)}
                          className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
                        >
                          Save
                        </button>
                        <button
                          onClick={() => setEditingTask(null)}
                          className="px-3 py-1 bg-gray-500 text-white rounded hover:bg-gray-600"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    // Display mode
                    <div>
                      <div className="flex items-start justify-between">
                        <div className="flex items-start space-x-3">
                          <input
                            type="checkbox"
                            checked={task.completed}
                            onChange={() => toggleTaskCompletion(task.id, task.completed)}
                            className="mt-1 h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500"
                          />
                          <div>
                            <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                              {task.title}
                            </h3>
                            {task.description && (
                              <p className={`text-sm mt-1 ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                                {task.description}
                              </p>
                            )}
                            <p className="text-xs text-gray-500 mt-1">
                              Created: {new Date(task.created_at).toLocaleDateString()}
                            </p>
                          </div>
                        </div>
                        <div className="flex space-x-2">
                          <button
                            onClick={() => setEditingTask(task)}
                            className="p-2 text-blue-600 hover:text-blue-800"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                            </svg>
                          </button>
                          <button
                            onClick={() => deleteTask(task.id)}
                            className="p-2 text-red-600 hover:text-red-800"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default DashboardPage;
'''
        return dashboard_page_content

    def generate_api_client(self):
        """Generate the API client for backend communication."""
        api_client_content = '''// API Client for communicating with backend
class APIClient {
  constructor(baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') {
    this.baseURL = baseURL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    // Add auth token if available
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    return response.json();
  }

  // Auth endpoints
  async signup(email, password) {
    return this.request('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async login(email, password) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  // Task endpoints
  async getTasks() {
    return this.request('/todos/');
  }

  async createTask(title, description) {
    return this.request('/todos/', {
      method: 'POST',
      body: JSON.stringify({ title, description }),
    });
  }

  async updateTask(taskId, data) {
    return this.request(`/todos/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteTask(taskId) {
    return this.request(`/todos/${taskId}`, {
      method: 'DELETE',
    });
  }
}

export default new APIClient();
'''
        return api_client_content


class FrontendAgent:
    """Frontend agent for building the Next.js web application."""

    def __init__(self):
        self.component_generator = NextJSComponentGenerator()
        self.project_structure = {
            "pages": {
                "index.js": self._generate_home_page(),
                "login.js": "",
                "signup.js": "",
                "dashboard.js": ""
            },
            "components": {
                "Layout.js": "",
                "Header.js": "",
            },
            "contexts": {
                "AuthContext.js": ""
            },
            "lib": {
                "apiClient.js": ""
            },
            "styles": {
                "globals.css": self._generate_global_styles()
            }
        }

    def _generate_home_page(self):
        """Generate the home page."""
        return '''import React from 'react';
import Link from 'next/link';
import Layout from '../components/Layout';

const HomePage = () => {
  return (
    <Layout title="Todo App - Home">
      <div className="text-center max-w-2xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-6">
          Welcome to Todo App
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Manage your tasks efficiently with our beautiful and intuitive interface.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/signup"
            className="px-8 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-lg font-medium"
          >
            Get Started
          </Link>
          <Link
            href="/login"
            className="px-8 py-3 bg-white text-indigo-600 border border-indigo-600 rounded-lg hover:bg-indigo-50 transition-colors text-lg font-medium"
          >
            Sign In
          </Link>
        </div>

        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Organize</h3>
            <p className="text-gray-600">Keep all your tasks organized in one place</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Collaborate</h3>
            <p className="text-gray-600">Work together with your team seamlessly</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Achieve</h3>
            <p className="text-gray-600">Complete tasks and achieve your goals</p>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default HomePage;
'''

    def _generate_global_styles(self):
        """Generate global CSS styles."""
        return '''@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground-rgb: 255, 255, 255;
    --background-start-rgb: 0, 0, 0;
    --background-end-rgb: 0, 0, 0;
  }
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
      to bottom,
      transparent,
      rgb(var(--background-end-rgb))
    )
    rgb(var(--background-start-rgb));
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c5c5c5;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Animation for task items */
.task-item {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
'''

    def generate_nextjs_project(self):
        """Generate the complete Next.js project structure and files."""
        # Generate all components
        self.project_structure["components"]["Layout.js"] = self.component_generator.generate_layout_component()
        self.project_structure["components"]["Header.js"] = self.component_generator.generate_header_component()
        self.project_structure["contexts"]["AuthContext.js"] = self.component_generator.generate_auth_context()
        self.project_structure["pages"]["login.js"] = self.component_generator.generate_login_page()
        self.project_structure["pages"]["signup.js"] = self.component_generator.generate_signup_page()
        self.project_structure["pages"]["dashboard.js"] = self.component_generator.generate_dashboard_page()
        self.project_structure["lib"]["apiClient.js"] = self.component_generator.generate_api_client()

        return self.project_structure

    def create_project_files(self, base_dir="./frontend"):
        """Create the actual project files."""
        import os

        # Create directory structure
        os.makedirs(os.path.join(base_dir, "pages"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "components"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "contexts"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "lib"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "styles"), exist_ok=True)

        # Write files
        for dir_name, files in self.project_structure.items():
            for file_name, content in files.items():
                file_path = os.path.join(base_dir, dir_name, file_name)
                with open(file_path, 'w') as f:
                    f.write(content)

        # Create package.json
        package_json = {
            "name": "todo-frontend",
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            },
            "dependencies": {
                "next": "14.0.0",
                "react": "^18",
                "react-dom": "^18"
            },
            "devDependencies": {
                "autoprefixer": "^10.4.16",
                "postcss": "^8.4.31",
                "tailwindcss": "^3.3.3"
            }
        }

        with open(os.path.join(base_dir, "package.json"), 'w') as f:
            import json
            json.dump(package_json, f, indent=2)

        # Create tailwind.config.js
        tailwind_config = '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
'''
        with open(os.path.join(base_dir, "tailwind.config.js"), 'w') as f:
            f.write(tailwind_config)

        # Create postcss.config.js
        postcss_config = '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
'''
        with open(os.path.join(base_dir, "postcss.config.js"), 'w') as f:
            f.write(postcss_config)


# Global frontend agent instance
frontend_agent = FrontendAgent()