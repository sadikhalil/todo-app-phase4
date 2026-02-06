/** @type {import('next').NextConfig} */
const nextConfig = {
  // Root directory to prevent warnings about multiple lockfiles
  // This addresses the workspace root inference warning
  experimental: {
    // This property helps Next.js identify the correct workspace root
    // when multiple lockfiles are detected
  },
};

// Since the experimental.turbopack.root approach caused errors,
// we'll resolve the issue by removing the conflicting lockfile
// and letting Next.js naturally detect the correct root

module.exports = nextConfig;