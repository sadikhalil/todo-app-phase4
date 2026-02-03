import React from 'react';
import { toast } from 'react-hot-toast';
import { CheckCircle, AlertCircle, Info, X } from 'lucide-react';
import { motion } from 'framer-motion';

interface ToastProps {
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
}

const ToastComponent: React.FC<ToastProps> = ({ message, type }) => {
  const getIcon = () => {
    switch (type) {
      case 'success':
        return <CheckCircle className="text-green-500" size={20} />;
      case 'error':
        return <AlertCircle className="text-red-500" size={20} />;
      case 'warning':
        return <AlertCircle className="text-yellow-500" size={20} />;
      case 'info':
        return <Info className="text-blue-500" size={20} />;
      default:
        return <Info className="text-blue-500" size={20} />;
    }
  };

  const getBackground = () => {
    switch (type) {
      case 'success':
        return 'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800';
      case 'error':
        return 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800';
      case 'warning':
        return 'bg-yellow-50 border-yellow-200 dark:bg-yellow-900/20 dark:border-yellow-800';
      case 'info':
        return 'bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800';
      default:
        return 'bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 300, scale: 0.8 }}
      animate={{ opacity: 1, x: 0, scale: 1 }}
      exit={{ opacity: 0, x: 300, scale: 0.8 }}
      className={`flex items-start p-4 rounded-lg border shadow-lg max-w-sm ${getBackground()}`}
    >
      <div className="mr-3 mt-0.5">
        {getIcon()}
      </div>
      <div className="flex-1 text-sm text-gray-800 dark:text-gray-200">
        {message}
      </div>
      <button
        onClick={() => toast.dismiss()}
        className="ml-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        aria-label="Close notification"
      >
        <X size={16} />
      </button>
    </motion.div>
  );
};

export const showToast = (message: string, type: 'success' | 'error' | 'warning' | 'info' = 'info') => {
  toast.custom(() => (
    <ToastComponent message={message} type={type} />
  ));
};

export default ToastComponent;