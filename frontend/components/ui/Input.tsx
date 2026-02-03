import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  animated?: boolean;
  className?: string;
}

const Input: React.FC<InputProps> = ({
  label,
  error,
  helperText,
  animated = false,
  className = '',
  ...props
}) => {
  const baseClasses = 'w-full px-4 py-2.5 rounded-lg border focus:outline-none focus:ring-2 transition-all duration-200';

  const inputClasses = `
    ${baseClasses}
    ${error
      ? 'border-red-500 focus:ring-red-200 focus:border-red-500 dark:focus:ring-red-900'
      : 'border-gray-300 focus:ring-blue-200 focus:border-blue-500 dark:border-gray-600 dark:focus:ring-blue-900'}
    ${className}
    bg-white dark:bg-gray-800 text-gray-900 dark:text-white
  `;

  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          {label}
        </label>
      )}
      <input
        className={inputClasses}
        {...props}
      />
      {helperText && !error && (
        <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
          {helperText}
        </p>
      )}
      {error && (
        <p className="mt-1 text-xs text-red-500">
          {error}
        </p>
      )}
    </div>
  );
};

export default Input;