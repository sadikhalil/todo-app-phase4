import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

const Sidebar = ({ user, onLogout }) => {
  const router = useRouter();

  const isActive = (path) => {
    return router.pathname === path;
  };

  const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: '📊' },
    { name: 'Tasks', href: '/dashboard', icon: '✅' },
    { name: 'Chat', href: '/chat', icon: '💬' },
    { name: 'Settings', href: '/settings', icon: '⚙️' },
  ];

  return (
    <aside className="fixed inset-y-0 left-0 z-40 w-64 bg-navy-blue text-white shadow-lg flex flex-col">
      {/* User Profile Section */}
      <div className="p-6 border-b border-gray-700">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-peach rounded-full flex items-center justify-center text-navy-blue font-bold">
            {user?.email?.charAt(0)?.toUpperCase() || 'U'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">{user?.email || 'User'}</p>
            <p className="text-xs text-gray-300 truncate">Member</p>
          </div>
        </div>
      </div>

      {/* Navigation Items */}
      <nav className="flex-1 py-4">
        <ul className="space-y-1 px-3">
          {navItems.map((item) => (
            <li key={item.href}>
              <Link
                href={item.href}
                className={`flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors duration-200 ${
                  isActive(item.href)
                    ? 'bg-peach text-navy-blue'
                    : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                }`}
              >
                <span className="text-lg">{item.icon}</span>
                <span>{item.name}</span>
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      {/* Logout Button */}
      <div className="p-4 border-t border-gray-700">
        <button
          onClick={onLogout}
          className="w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white transition-colors duration-200"
        >
          <span className="text-lg">🚪</span>
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;