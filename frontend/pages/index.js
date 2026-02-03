import React from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { TodoProvider } from '../contexts/TodoContext';
import ThemeToggle from '../components/ThemeToggle';
import { Toaster } from 'react-hot-toast';

const HomePage = () => {
  return (
    <>
      <Head>
        <title>Modern Todo App - Stay Organized</title>
        <meta name="description" content="A modern, interactive todo application" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <TodoProvider>
        <div className="min-h-screen bg-white dark:bg-navy-blue text-navy-blue dark:text-white transition-colors duration-200">
          {/* Navbar */}
          <nav className="bg-navy-blue text-white shadow-sm border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">
            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between items-center h-16">
                <div className="flex items-center">
                  <Link href="/" className="text-2xl font-bold text-white font-semibold">
                    Modern Todo App
                  </Link>
                </div>

                <div className="flex items-center space-x-4">
                  <Link
                    href="/login"
                    className="bg-peach text-navy-blue px-6 py-2 rounded-lg font-medium transition-all duration-200 hover:scale-105 shadow-md hover:shadow-lg hover:bg-orange hover:text-white"
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/signup"
                    className="bg-orange text-white px-6 py-2 rounded-lg font-medium transition-all duration-200 hover:scale-105 shadow-md hover:shadow-lg hover:bg-peach hover:text-navy-blue"
                  >
                    Sign Up
                  </Link>
                  <ThemeToggle className="p-2.5 rounded-full bg-orange text-white hover:bg-peach transition-all duration-200 hover:scale-105 shadow-md" />
                </div>
              </div>
            </div>
          </nav>

          {/* Welcome Section */}
          <div className="max-w-4xl mx-auto px-4 py-16">
            <div className="text-center mb-16">
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="mb-8"
              >
                <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-navy-blue dark:text-white mb-6">
                  Welcome to Modern Todo App
                </h1>
                <p className="text-lg md:text-xl lg:text-2xl text-navy-blue dark:text-white max-w-3xl mx-auto leading-relaxed">
                  A beautifully designed, highly interactive todo application with smooth animations,
                  drag-and-drop reordering, and a seamless user experience. Organize your tasks with style and boost your productivity.
                </p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="flex flex-col sm:flex-row gap-6 justify-center items-center mt-8"
              >
                <Link
                  href="/signup"
                  className="bg-navy-blue text-white font-bold py-4 px-10 rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-110 text-lg sm:text-xl min-w-[240px] hover:bg-orange hover:text-white"
                >
                  Get Started
                </Link>
                <Link
                  href="/todo"
                  className="bg-peach text-navy-blue font-bold py-4 px-10 rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-110 text-lg sm:text-xl min-w-[240px] hover:bg-orange hover:text-white"
                >
                  Try Demo
                </Link>
              </motion.div>
            </div>

            {/* Features Grid */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 mb-16"
            >
              <div className="bg-white dark:bg-peach rounded-2xl shadow-lg p-6 hover:shadow-2xl transition-all duration-300 border border-gray-200 dark:border-gray-700 transform hover:-translate-y-1">
                <div className="w-12 h-12 bg-navy-blue rounded-xl flex items-center justify-center mx-auto mb-4 shadow-md">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-lg sm:text-xl font-bold text-navy-blue dark:text-white mb-3">Lightning Fast</h3>
                <p className="text-sm md:text-base text-navy-blue dark:text-gray-400">Experience smooth animations and instant task management with our optimized performance.</p>
              </div>

              <div className="bg-white dark:bg-peach rounded-2xl shadow-lg p-6 hover:shadow-2xl transition-all duration-300 border border-gray-200 dark:border-gray-700 transform hover:-translate-y-1">
                <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl flex items-center justify-center mx-auto mb-4 shadow-md">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <h3 className="text-lg sm:text-xl font-bold text-navy-blue dark:text-white mb-3">Secure & Private</h3>
                <p className="text-sm md:text-base text-navy-blue dark:text-gray-400">Your tasks are stored securely with end-to-end encryption and privacy protection.</p>
              </div>

              <div className="bg-white dark:bg-peach rounded-2xl shadow-lg p-6 hover:shadow-2xl transition-all duration-300 border border-gray-200 dark:border-gray-700 transform hover:-translate-y-1">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mx-auto mb-4 shadow-md">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4h4a2 2 0 002-2V5z" />
                  </svg>
                </div>
                <h3 className="text-lg sm:text-xl font-bold text-navy-blue dark:text-white mb-3">Cross Platform</h3>
                <p className="text-sm md:text-base text-navy-blue dark:text-gray-400">Access your tasks seamlessly across all your devices with real-time synchronization.</p>
              </div>
            </motion.div>
          </div>

          {/* Footer */}
          <footer className="bg-navy-blue text-white border-t-2 border-gray-200 py-12">
            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="text-center">
                <div className="mb-6">
                  <h3 className="text-xl font-bold text-white mb-4">Contact the Creator</h3>
                  <div className="flex flex-col sm:flex-row justify-center items-center gap-6 text-white">
                    <div className="flex items-center space-x-3 bg-peach text-navy-blue rounded-xl px-4 py-2 shadow-md hover:shadow-lg transition-shadow duration-300">
                      <svg className="w-5 h-5 text-gray-900 dark:text-white" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                      </svg>
                      <span className="font-medium">
                        <a
                          href="https://github.com/sadikhalil"
                          target="_blank"
                          rel="noopener noreferrer"
                          className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                        >
                          https://github.com/sadikhalil
                        </a>
                      </span>
                    </div>
                    <div className="flex items-center space-x-3 bg-peach text-navy-blue rounded-xl px-4 py-2 shadow-md hover:shadow-lg transition-shadow duration-300">
                      <svg className="w-5 h-5 text-gray-900 dark:text-white" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819v-6.656l-2.001 1.664-2.001-1.664v6.656h-3.819c-.904 0-1.636-.732-1.636-1.636v-5.188l-4.421 3.701c-.36.299-.86.468-1.412.468-.552 0-1.052-.169-1.413-.468l-4.421-3.701v5.188c0 .904-.732 1.636-1.636 1.636h-3.819c-.904 0-1.636-.732-1.636-1.636v-13.909c0-.904.732-1.636 1.636-1.636h3.819v6.656l2.001-1.664 2.001 1.664v-6.656h3.819c.904 0 1.636.732 1.636 1.636v5.188l4.421-3.701c.36-.299.86-.468 1.412-.468.552 0 1.052.169 1.413.468l4.421 3.701v-5.188c0-.904.732-1.636 1.636-1.636h3.819c.904 0 1.636.732 1.636 1.636z"/>
                      </svg>
                      <span className="font-medium">sadiakhalil0223@gmail.com</span>
                    </div>
                  </div>
                </div>
                <div className="text-sm text-navy-blue dark:text-gray-400 font-medium">
                  © {new Date().getFullYear()} Modern Todo App. All rights reserved.
                </div>
              </div>
            </div>
          </footer>

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
        </div>
      </TodoProvider>
    </>
  );
};

export default HomePage;