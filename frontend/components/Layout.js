import React from 'react';
import Head from 'next/head';
import { useAuth } from '../contexts/AuthContext';
import Sidebar from './Sidebar';

const Layout = ({ children, title = "My Tasks", showSidebar = false }) => {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-white dark:bg-navy-blue text-navy-blue dark:text-white flex">
        {showSidebar && user && (
          <Sidebar user={user} onLogout={handleLogout} />
        )}

        <main className={`${showSidebar ? 'ml-64' : ''} flex-1 container mx-auto px-4 py-8 max-w-6xl`}>
          {children}
        </main>
      </div>
    </>
  );
};

export default Layout;
