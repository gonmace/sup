module.exports = {
    content: [
        '../../templates/*.html',
        '../../templates/**/*.html', 
        '../../main/src/index-main.js',
        '../../**/templates/*.html',  
        '!../../**/node_modules',
        '../../**/src/*.js',
        
        '../../**/templates/**/*.html',  
    ],
    plugins: [
        require('daisyui'),
        // require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('tailwindcss-neumorphism-ui'),
    ],
    daisyui: {
        themes: [
          {
            mytheme: {
              "primary": "#FF4444",
              "secondary": "#00D400",
              "accent": "#3b82f6",
              "neutral": "#3d4451",
              "base-100": "#fffff8",
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
