/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx}',
    './src/components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3f8cff',
        secondary: '#f50057',
        background: '#0d1117',
        paper: '#161b22',
      },
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false,
  },
  important: '#__next',
};