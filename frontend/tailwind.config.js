/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: {
          950: '#000000',
          900: '#0A0A0A',
          850: '#0F0F10',
          800: '#141415',
          700: '#1C1C1E',
          border: 'rgba(255,255,255,0.08)',
          borderStrong: 'rgba(255,255,255,0.14)'
        },
        text: {
          primary: '#F3F2EF',
          secondary: '#8D8D93',
          tertiary: '#5B5B60'
        },
        accent: {
          violet: '#B4A5F5',
          blue: '#8FB1E8'
        },
        positive: {
          DEFAULT: '#5FCB9B',
          soft: 'rgba(95,203,155,0.10)',
          border: 'rgba(95,203,155,0.28)',
          text: '#8EDCB6'
        },
        negative: {
          DEFAULT: '#E38A93',
          soft: 'rgba(227,138,147,0.10)',
          border: 'rgba(227,138,147,0.28)',
          text: '#E9A5AC'
        }
      },
      fontFamily: {
        display: ['"Fraunces"', 'serif'],
        body: ['"Inter"', 'system-ui', 'sans-serif']
      },
      keyframes: {
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(14px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        resultReveal: {
          '0%': { opacity: '0', transform: 'translateY(18px) scale(0.98)' },
          '100%': { opacity: '1', transform: 'translateY(0) scale(1)' }
        },
        emojiPop: {
          '0%': { opacity: '0', transform: 'scale(0.5)' },
          '60%': { opacity: '1', transform: 'scale(1.08)' },
          '100%': { opacity: '1', transform: 'scale(1)' }
        },
        drift: {
          '0%, 100%': { transform: 'translateX(0)' },
          '50%': { transform: 'translateX(-14px)' }
        },
        pulseSoft: {
          '0%, 100%': { opacity: '0.35' },
          '50%': { opacity: '0.7' }
        }
      },
      animation: {
        fadeUp: 'fadeUp 0.7s cubic-bezier(0.16,1,0.3,1) both',
        resultReveal: 'resultReveal 0.6s cubic-bezier(0.16,1,0.3,1) both',
        emojiPop: 'emojiPop 0.55s cubic-bezier(0.34,1.56,0.64,1) both',
        drift: 'drift 12s ease-in-out infinite',
        pulseSoft: 'pulseSoft 2.4s ease-in-out infinite'
      }
    }
  },
  plugins: []
}
