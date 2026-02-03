import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  ripple?: boolean;
  children: React.ReactNode;
  className?: string;
}

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  ripple = false,
  children,
  className = '',
  ...props
}) => {
  const baseClasses = 'font-medium rounded-lg transition-all duration-200 inline-flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed hover:transform hover:scale-105 active:scale-95';

  const sizeClasses = {
    sm: 'text-sm py-2 px-4',
    md: 'text-base py-2.5 px-5',
    lg: 'text-lg py-3 px-6',
  };

  const variantClasses = {
    primary: 'bg-blue-500 hover:bg-blue-600 text-white shadow-md hover:shadow-lg',
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800 shadow-sm hover:shadow-md dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-white',
    danger: 'bg-red-500 hover:bg-red-600 text-white shadow-md hover:shadow-lg',
    ghost: 'bg-transparent hover:bg-gray-100 text-gray-700 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-700',
  };

  const classes = `${baseClasses} ${sizeClasses[size]} ${variantClasses[variant]} ${className}`;

  return (
    <button
      className={classes}
      disabled={isLoading}
      {...props}
    >
      {isLoading ? (
        <span className="flex items-center justify-center">
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Loading...
        </span>
      ) : (
        children
      )}
    </button>
  );
};

export default Button;