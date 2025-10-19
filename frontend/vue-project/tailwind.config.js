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
			"cat-header": "#43433F",
			"cat-bg": "#D9D2D2",

			"neutral": {
				200: "#E9ECEF",
				400: "#CED4DA",
				"white": "#FFFFFF",
			},

			"breadcrumbs": {
				"inactive": "#6C757D",
				"active": "#212529",

				"light": {
					"inactive": "#D9D9D9",
					"active": "#FFFFFF"
				}
			},

			"text": {
				"disabled": "#ADB5BD",
				"normal": "#343A40",
				"heading": "#212529",
				"button": "#FFFFFF",
				"secondary": "#6C757D"
			},

			"primary": {
				"normal": "#0057FC"
			},

			"sex": {
				"male": "#6aa2f7",
				"female": "#f990c7"
			},

			"border": {
				"group": "#D9D9D9",
			}
		},
		screens: {
			"2md": "968px"
		}
	},
  },
  plugins: [],
}

