import React, { useState, useEffect, useRef } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { motion } from 'framer-motion';
import apiClient from '../lib/apiClient';
import { useTodo } from '../contexts/TodoContext';

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const [userId, setUserId] = useState(null);
  const messagesEndRef = useRef(null);
  const router = useRouter();
  const { refreshTodos } = useTodo(); // Get the refreshTodos function from TodoContext

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Check if user is authenticated
  useEffect(() => {
    const token = localStorage.getItem('token');
    const storedUserId = localStorage.getItem('userId');

    if (!token || !storedUserId) {
      router.push('/login');
      return;
    }

    setUserId(storedUserId);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading) return;

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // Use the API client to make the chat request
      // The backend mounts the API router at /api, so the full path is /api/{userId}/chat
      const data = await apiClient.request(`/api/${userId}/chat`, {
        method: 'POST',
        body: JSON.stringify({
          conversation_id: conversationId,
          message: inputValue
        })
      });

      // Update conversation ID if it was created
      if (data.conversation_id && !conversationId) {
        setConversationId(data.conversation_id);
      }

      // Add assistant message
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString(),
        tool_calls: data.tool_calls || []
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Refresh todos to reflect any changes made through the chat
      console.log('About to refresh todos after chat operation...');
      console.log('Data received from backend:', data); // Debug log
      setTimeout(() => {
        console.log('Calling refreshTodos...');
        refreshTodos().then(() => {
          console.log('refreshTodos completed');
        }).catch(error => {
          console.error('Error in refreshTodos:', error);
        });
      }, 500); // Small delay to ensure the backend has processed the request
    } catch (err) {
      setError(err.message);
      console.error('Chat error:', err);
      console.log('Error occurred during chat processing, refreshTodos may not execute');

      // Add error message to UI
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

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex flex-col h-full">
      <Head>
        <title>AI Todo Chat - Modern Todo App</title>
        <meta name="description" content="Chat with your AI productivity assistant" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="flex-1 flex flex-col bg-white dark:bg-navy-blue text-navy-blue dark:text-white transition-colors duration-200">

        {/* Chat Container */}
        <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full px-4 py-6">
          <div className="mb-6 text-center">
            <h1 className="text-3xl font-bold text-navy-blue dark:text-white mb-2">
              AI Todo Assistant
            </h1>
            <p className="text-navy-blue dark:text-gray-300">
              Chat with your AI productivity assistant to manage tasks naturally
            </p>
            {conversationId && (
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                Conversation ID: {conversationId}
              </p>
            )}
          </div>

          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto max-h-[calc(100vh-250px)] mb-4 space-y-4">
            {messages.length === 0 ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-navy-blue rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-navy-blue dark:text-white mb-2">
                  Start a conversation
                </h3>
                <p className="text-navy-blue dark:text-gray-300 max-w-md mx-auto">
                  Try commands like "Add a task to buy groceries", "Show my tasks", or "Complete task 1".
                </p>
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
                    className={`max-w-xs sm:max-w-md lg:max-w-lg xl:max-w-xl px-4 py-3 rounded-2xl ${
                      message.role === 'user'
                        ? 'bg-navy-blue text-white ml-12'
                        : message.isError
                        ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100 mr-12'
                        : 'bg-peach text-navy-blue mr-12'
                    }`}
                  >
                    <div className="whitespace-pre-wrap break-words">{message.content}</div>
                    {message.tool_calls && message.tool_calls.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-current/20 text-xs opacity-75">
                        Actions taken: {message.tool_calls.map(tc => tc.name).join(', ')}
                      </div>
                    )}
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
                <div className="bg-peach text-navy-blue mr-12 px-4 py-3 rounded-2xl">
                  <div className="flex items-center space-x-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-navy-blue rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-navy-blue rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-navy-blue rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                    <span>Thinking...</span>
                  </div>
                </div>
              </motion.div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="relative">
            {error && (
              <div className="mb-3 p-3 bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100 rounded-lg text-sm">
                Error: {error}
              </div>
            )}
            <div className="flex space-x-3">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type your message... (e.g., 'Add a task to buy groceries')"
                disabled={isLoading}
                className="flex-1 resize-none rounded-2xl border border-gray-300 dark:border-gray-600 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-navy-blue focus:border-transparent bg-white dark:bg-navy-blue text-navy-blue dark:text-white placeholder-gray-500 dark:placeholder-gray-400 min-h-[60px] max-h-32"
                rows={1}
              />
              <button
                type="submit"
                disabled={!inputValue.trim() || isLoading}
                className="bg-navy-blue text-white px-6 py-3 rounded-2xl font-medium transition-all duration-200 hover:scale-105 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                Send
              </button>
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
              Try: "Add task", "Show tasks", "Complete task 1", "Delete task"
            </p>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;