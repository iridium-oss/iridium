/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  eslint: { ignoreDuringBuilds: true },
  typescript: { ignoreBuildErrors: false },
  async rewrites() {
    return [
      { source: '/api/:path*', destination: 'http://localhost:8000/api/:path*' },
      { source: '/health', destination: 'http://localhost:8000/health' },
      { source: '/version', destination: 'http://localhost:8000/version' },
    ];
  },
};

module.exports = nextConfig;
