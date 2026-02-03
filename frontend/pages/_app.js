import React from 'react';
import '../styles/globals.css'; // Import global styles
import { AuthProvider } from '../contexts/AuthContext';
import { TodoProvider } from '../contexts/TodoContext';
import { Toaster } from 'react-hot-toast';

// Custom App component to wrap all pages with providers
function MyApp({ Component, pageProps }) {
  return (
    <AuthProvider>
      <TodoProvider>
      <Component {...pageProps} />
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
      </TodoProvider>
    </AuthProvider>
  );
}

export default MyApp;