import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTodo } from '../contexts/TodoContext';

// Helper function to safely get token from localStorage
const getToken = () => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('access_token') || localStorage.getItem('token');
  }
  return null;
};

const FloatingChatButton = ({ userId, userToken }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { refreshTodos } = useTodo(); // Hook to refresh tasks after chat operations

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${BASE_URL}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${userToken}`
        },
        body: JSON.stringify({
          message: inputValue,
          user_id: userId
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Check if the original user message contained task-related commands to trigger refresh
      const userInput = inputValue.toLowerCase();
      const hasTaskCommand = userInput.includes('add task') ||
                            userInput.includes('add a task') ||
                            userInput.includes('create task') ||
                            userInput.includes('create a task') ||
                            userInput.includes('delete task') ||
                            userInput.includes('delete the task') ||
                            userInput.includes('complete task') ||
                            userInput.includes('mark task') ||
                            userInput.includes('update task') ||
                            userInput.includes('edit task');

      if (hasTaskCommand) {
        // Small delay to ensure the backend operation completes before refreshing
        setTimeout(async () => {
          try {
            console.log('Refreshing tasks after chat operation...');
            await refreshTodos();
            console.log('Tasks refreshed successfully');
          } catch (error) {
            console.error('Failed to refresh tasks after chat operation:', error);
            // Retry after a short delay if it fails
            setTimeout(async () => {
              try {
                await refreshTodos();
              } catch (retryError) {
                console.error('Retry to refresh tasks also failed:', retryError);
              }
            }, 1500);
          }
        }, 800); // Reduced delay to make it more responsive
      }
    } catch (err) {
      const errorMessage = {
        id: Date.now(),
        role: 'assistant',
        content: `Sorry, I encountered an error: ${err.message}`,
        timestamp: new Date().toISOString(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <>
      {/* Floating Chat Button */}
      <motion.button
        onClick={toggleChat}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-navy-blue text-white rounded-full shadow-lg flex items-center justify-center hover:bg-orange hover:text-navy-blue transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-navy-blue floating-chat-button"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        aria-label="Open chat"
      >
        💬
      </motion.button>

      {/* Chat Modal */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-end justify-end p-4 pointer-events-none"
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0, y: 50 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.8, opacity: 0, y: 50 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              className="pointer-events-auto w-full max-w-md h-96 bg-white dark:bg-navy-blue rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 flex flex-col"
            >
              {/* Chat Header */}
              <div className="bg-navy-blue text-white p-4 rounded-t-lg flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="text-lg">🤖</span>
                  <h3 className="font-semibold">AI Assistant</h3>
                </div>
                <button
                  onClick={toggleChat}
                  className="text-white hover:text-gray-300 focus:outline-none"
                >
                  ✕
                </button>
              </div>

              {/* Messages Container */}
              <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-white dark:bg-navy-blue">
                {messages.length === 0 ? (
                  <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                    <div className="w-12 h-12 bg-navy-blue text-white rounded-full flex items-center justify-center mx-auto mb-3">
                      💬
                    </div>
                    <p className="text-sm">Start a conversation with your AI assistant</p>
                  </div>
                ) : (
                  messages.map((message) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-xs px-3 py-2 rounded-lg text-sm ${
                          message.role === 'user'
                            ? 'bg-navy-blue text-white'
                            : message.isError
                            ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100'
                            : 'bg-peach text-navy-blue'
                        }`}
                      >
                        <div className="whitespace-pre-wrap break-words text-sm">{message.content}</div>
                        <div className={`text-xs mt-1 ${message.role === 'user' ? 'text-blue-100' : message.isError ? 'text-red-600 dark:text-red-300' : 'text-navy-blue/70'}`}>
                          {formatTimestamp(message.timestamp)}
                        </div>
                      </div>
                    </motion.div>
                  ))
                )}

                {isLoading && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex justify-start"
                  >
                    <div className="bg-peach text-navy-blue px-3 py-2 rounded-lg">
                      <div className="flex items-center space-x-2">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-navy-blue rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-navy-blue rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                          <div className="w-2 h-2 bg-navy-blue rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        </div>
                        <span>Typing...</span>
                      </div>
                    </div>
                  </motion.div>
                )}
              </div>

              {/* Input Form */}
              <form onSubmit={handleSubmit} className="border-t border-gray-200 dark:border-gray-700 p-3">
                <div className="flex space-x-2">
                  <input
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Type your message..."
                    disabled={isLoading}
                    className="flex-1 px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-navy-blue focus:border-transparent bg-white dark:bg-navy-blue text-navy-blue dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                  />
                  <button
                    type="submit"
                    disabled={!inputValue.trim() || isLoading}
                    className="bg-navy-blue text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200 hover:bg-orange hover:text-navy-blue disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Send
                  </button>
                </div>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default FloatingChatButton;