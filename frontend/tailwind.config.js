module.exports = {
  mode: 'jit',
  purge: ['./src/**/*.ts', './src/**/*.tsx', './src/**/*.js', './src/**/*.jsx'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    rotate: {
      '-20': '-20deg',
      '-10': '-10deg',
      0: '0',
      10: '10deg',
      20: '20deg',
    },
    extend: {
      fontFamily: {
        'alfa-slab-one': ['"Alfa Slab One"', 'cursive'],
        'courier-prime': ['"Courier Prime"', 'monospace'],
      },
      colors: {
        gold: '#edc742',
        grass: '#0e7c20',
        'grass-dark': '#073b1d',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
