import React, { ReactNode } from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import ThemeToggle from './ThemeToggle';

interface LayoutProps {
  children: ReactNode;
  title?: string;
  description?: string;
}

const Layout: React.FC<LayoutProps> = ({ children, title = 'Modern Todo App', description = 'A modern, interactive todo application' }) => {
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="description" content={description} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
        className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 text-gray-900 dark:text-gray-100 transition-colors duration-200"
      >
        <div className="max-w-4xl mx-auto px-4 py-8">
          {/* Skip link for accessibility */}
          <a
            href="#main-content"
            className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:bg-blue-500 focus:text-white focus:px-4 focus:py-2 focus:rounded-lg"
          >
            Skip to main content
          </a>

          <header className="flex justify-between items-center mb-12">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-600">
                {title}
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-1">
                Organize your tasks with style
              </p>
            </div>

            <ThemeToggle className="p-2 rounded-full bg-white dark:bg-gray-800 shadow-md" />
          </header>

          <main id="main-content" className="flex flex-col items-center">
            {children}
          </main>

          <footer className="mt-16 text-center text-gray-500 dark:text-gray-400 text-sm">
            <p>Drag and drop to reorder tasks • Double-click to edit</p>
          </footer>
        </div>
      </motion.div>
    </>
  );
};

export default Layout;