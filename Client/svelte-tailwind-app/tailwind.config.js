module.exports = {
  content: [
    './src/**/*.{html,js,svelte}',           // All svelte, html, js files inside src
    './public/index.html',                   // If index.html exists inside public folder
    './src/components/**/*.{svelte,ts}',     // Ensure all components are considered
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
