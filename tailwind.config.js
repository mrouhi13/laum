module.exports = {
  purge: ['./components/**/*.{js,ts,jsx,tsx}', './pages/**/*.{js,ts,jsx,tsx}'],
  theme: {
    fontFamily: {
      body: ['Cormorant\\ Infant', 'serif']
    },
    screens: {
      xxl: '1600px',
      xl: '1200px',
      lg: '992px',
      md: '768px',
      sm: '576px',
      xs: '480px',
      xxs: { max: '479px' }
    },
    extend: {
      colors: {
        gold: '#FFD700',
        overlay: '#141414',
        brown: '#B55400',
        'light-brown': '#B67929',
        'jet-black': '#0A0A0A',
        link: '#73767A',
        'link-hover': '#171616'
      },
      spacing: {
        72: '18rem',
        84: '21rem',
        96: '24rem',
        112: '28rem'
      },
      borderRadius: {
        xl: '0.75rem',
        xxl: '1rem'
      },
      boxShadow: {
        navbar: '0 1px 2px 0 rgba(0, 0, 0, .16), 0 0 0 0 rgba(0, 0, 0, .08)',
        'navbar-focus':
          '0 2px 3px 0 rgba(0, 0, 0, .16), 0 0 0 0 rgba(0, 0, 0, .08)'
      }
    }
  },
  variants: {},
  plugins: [],
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true
  }
}
