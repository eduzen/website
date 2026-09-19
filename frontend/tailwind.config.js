/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../blog/templates/**/*.html",
    "../core/templates/**/*.html",
    "../blog/**/*.py",
    "../core/**/*.py",
    "../website/**/*.py",
    "../.venv/lib/python*/site-packages/crispy_tailwind/**/*.html",
    "/opt/venv/lib/python*/site-packages/crispy_tailwind/**/*.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
