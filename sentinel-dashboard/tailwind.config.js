import plugin from 'tailwindcss/plugin'
module.exports = {
  darkMode: "class", // Enable class-based dark mode
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],

  plugins: [
    plugin(function({addVariant}){
        addVariant('hover-focus', ['&:hover', '&:focus'])
    })
  ],
  
  theme: {
    extend: {
      colors: {
        secondary: {
            50:  '#EEF3FE',
            100: '#D9E3FC',
            200: '#B5C7F8',
            300: '#8BA7F4',
            400: '#5D84ED',
            500: '#2E60DC',
            600: '#264EB6',
            700: '#1E3D91',
            800: '#172E6E',
            900: '#0F204D',
          },
          primary: {
            50:  '#FFF7EE',
            100: '#FCEBD9',
            200: '#F6D2AF',
            300: '#EFB985',
            400: '#E59C5E',
            500: '#CC8446',
            600: '#A96A36',
            700: '#875428',
            800: '#633E1B',
            900: '#422A11',
          },
      },
    },
},

};
