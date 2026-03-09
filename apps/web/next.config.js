/** @type {import('next').NextConfig} */
const path = require('path');
const apiBaseUrl = process.env.IRIDIUM_API_INTERNAL_URL || 'http://localhost:8000';

const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  typescript: { ignoreBuildErrors: false },
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'upload.wikimedia.org', pathname: '/wikipedia/commons/**' },
      { protocol: 'https', hostname: 'commons.wikimedia.org', pathname: '/wiki/Special:Redirect/**' },
    ],
  },
  webpack: (config) => {
    config.resolve.alias['@'] = path.resolve(__dirname);
    return config;
  },
  async rewrites() {
    return [
      { source: '/api/:path*', destination: `${apiBaseUrl}/api/:path*` },
      { source: '/health', destination: `${apiBaseUrl}/health` },
      { source: '/version', destination: `${apiBaseUrl}/version` },
    ];
  },
};

module.exports = nextConfig;
