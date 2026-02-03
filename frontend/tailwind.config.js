/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'navy-blue': '#1B1F3B',  // Header/navigation bar background
        'orange': '#FF7F50',      // Primary action button, high-priority
        'peach': '#FFB199',       // Secondary buttons, medium-priority
        'white': '#FFFFFF',       // Text on navy, card backgrounds
        'text-navy': '#1B1F3B',   // Primary text on light backgrounds
        'text-white': '#FFFFFF',  // Text on navy backgrounds
        'background-primary': '#FFFFFF', // Clean white backgrounds
        'card-bg': '#FFFFFF',     // Card backgrounds for individual tasks
        'button-primary': '#FF7F50', // Orange for primary buttons
        'button-secondary': '#FFB199', // Peach for secondary buttons
        'priority-high': '#FF7F50', // Orange for high priority
        'priority-medium': '#FFB199', // Peach for medium priority
        'priority-low': '#1B1F3B', // Navy for low priority
      },
      animation: {
        'bounce': 'bounce 0.6s ease-in-out',
        'scale-pulse': 'scalePulse 0.3s ease-in-out',
        'glow': 'glow 2s infinite',
        'rotate': 'rotate 2s linear infinite',
        'slide-in': 'slideIn 0.3s ease-out',
      },
      keyframes: {
        bounce: {
          '0%, 20%, 50%, 80%, 100%': { transform: 'translateY(0)' },
          '40%': { transform: 'translateY(-10px)' },
          '60%': { transform: 'translateY(-5px)' },
        },
        scalePulse: {
          '0%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.05)' },
          '100%': { transform: 'scale(1)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 0 rgba(255, 107, 107, 0.3)' },
          '50%': { boxShadow: '0 0 20px rgba(255, 107, 107, 0.6)' },
          '100%': { boxShadow: '0 0 0 rgba(255, 107, 107, 0.3)' },
        },
        rotate: {
          from: { transform: 'rotate(0deg)' },
          to: { transform: 'rotate(360deg)' },
        },
        slideIn: {
          from: { opacity: 0, transform: 'translateY(20px) scale(0.95)' },
          to: { opacity: 1, transform: 'translateY(0) scale(1)' },
        },
      }
    },
  },
  darkMode: 'class',
  plugins: [],
};
