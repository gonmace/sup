module.exports = {
    content: [
        '../../templates/*.html',
        '../../templates/**/*.html', 
        '../../main/src/index-main.js',
        '../../**/templates/*.html',  
        '!../../**/node_modules',
    ],
    plugins: [
        require('daisyui'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
    daisyui: {
        themes: [
          {
            mytheme: {
              "primary": "#FF4444",
              "secondary": "#334263",
              "accent": "#fa0000",
              "neutral": "#3d4451",
              "base-100": "#fffff8",
              "terreno": "#fff5f5",
              "muro": "#fed7d7",
              "grava": "#feb2b2",
              "porton": "#fc8181",
              "pat": "#f56565",
              "electrico": "#e53e3e",
            },
          },
          "dark",
        ],
      },
      theme: {
        extend: {
          fontFamily: {
            'sans': ['nunito', 'sans-serif'],
          },
        },
      },
}
