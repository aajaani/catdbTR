/** @type {import('tailwindcss').Config} */

export default {
  content: [
	  "./index.html",
	  "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
	  colors: {
		  'nav-bg': '#363431',
		  'nav-li-bg': '#363431',
		  'nav-li-text': '#FFFFFF',
		  'nav-li-icon': '#FFFFFF',
		  'nav-li-selected': '#F8F9FA',
		  'nav-li-selected-text': '#000000',
		  'nav-li-selected-icon': '#000000',
		  'main-bg': '#F8F9FA',
		  'table-normal': '#343A40',
		  'table-secondary': '#6C757D',
		  'table-border': '#E9ECEF',

		  'neutral': {
			400: '#CED4DA',
		  }
	  }
	},
  },
  plugins: [],
}

