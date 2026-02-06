import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';

const SignupPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { signup } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    const result = await signup(email, password);

    if (!result.success) {
      setError(result.message);
      setLoading(false);
    }
  };

  return (
    <Layout title="Sign Up - Modern Todo App">
      <div className="max-w-md mx-auto bg-white dark:bg-peach text-navy-blue dark:text-navy-blue rounded-xl shadow-sm p-8">
        <h1 className="text-2xl font-bold text-center text-navy-blue dark:text-navy-blue mb-6">Create Account</h1>

        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-navy-blue dark:text-navy-blue mb-1">
              Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange focus:border-orange transition-colors duration-200"
              placeholder="your@email.com"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-navy-blue dark:text-navy-blue mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange focus:border-orange transition-colors duration-200"
              placeholder="••••••••"
            />
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-navy-blue dark:text-navy-blue mb-1">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange focus:border-orange transition-colors duration-200"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`
              w-full py-3 px-4 rounded-lg text-white font-medium
              ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-orange hover:bg-peach hover:text-navy-blue'}
              transition-colors duration-200
              ${loading ? 'pointer-events-none' : ''}
            `}
          >
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-navy-blue dark:text-navy-blue">
            Already have an account?{' '}
            <a href="/login" className="text-orange hover:text-peach font-medium">
              Sign in
            </a>
          </p>
        </div>
      </div>
    </Layout>
  );
};

export default SignupPage;
