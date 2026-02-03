import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/router';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in on initial load
    const storedToken = localStorage.getItem('access_token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const response = await fetch('http://localhost:8001/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));
        setToken(data.access_token);
        setUser(data.user);
        router.push('/todo'); // Redirect to todo page for task management
        return { success: true, message: 'Login successful' };
      } else {
        // Handle different error response formats
        let errorMessage = 'Invalid credentials';
        if (data && typeof data === 'object') {
          if (data.detail) {
            errorMessage = data.detail;
          } else if (data.message) {
            errorMessage = data.message;
          } else if (data.error) {
            errorMessage = data.error;
          }
        } else if (typeof data === 'string') {
          errorMessage = data;
        }
        return { success: false, message: errorMessage };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, message: 'An error occurred during login' };
    }
  };

  const signup = async (email, password) => {
    try {
      const response = await fetch('http://localhost:8001/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Backend returns access_token and user in the response
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));
        setToken(data.access_token);
        setUser(data.user);
        router.push('/todo'); // Redirect to todo page for task management
        return { success: true, message: 'Registration successful' };
      } else {
        // Handle different error response formats
        let errorMessage = 'Registration failed';
        if (data && typeof data === 'object') {
          if (data.detail) {
            errorMessage = data.detail;
          } else if (data.message) {
            errorMessage = data.message;
          } else if (data.error) {
            errorMessage = data.error;
          }
        } else if (typeof data === 'string') {
          errorMessage = data;
        }
        return { success: false, message: errorMessage };
      }
    } catch (error) {
      console.error('Signup error:', error);
      return { success: false, message: 'An error occurred during signup' };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
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
