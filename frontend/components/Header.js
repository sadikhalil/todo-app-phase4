import React from 'react';
import Link from 'next/link';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4 max-w-4xl flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-gray-900 hover:text-green-600 transition-colors duration-200">
          My Tasks
        </Link>

        <nav className="flex items-center space-x-4">
          <Link
            href="/login"
            className="text-gray-700 hover:text-green-600 font-medium px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors duration-200"
          >
            Sign In
          </Link>
          <Link
            href="/signup"
            className="bg-green-500 hover:bg-green-600 text-white font-medium px-4 py-2 rounded-lg shadow-sm hover:shadow-md transition-colors duration-200"
          >
            Get Started
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
