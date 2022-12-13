/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
	content: [
		/**
		 * HTML. Paths to Django template files that will contain Tailwind CSS classes.
		 */

		/*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
		"../templates/**/*.html",

		/*
		 * Main templates directory of the project (BASE_DIR/templates).
		 * Adjust the following line to match your project structure.
		 */
		"../../templates/**/*.html",

		/*
		 * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
		 * Adjust the following line to match your project structure.
		 */
		"../../**/templates/**/*.html",

		/**
		 * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
		 * patterns match your project structure.
		 */
		/* JS 1: Ignore any JavaScript in node_modules folder. */
		// '!../../**/node_modules',
		/* JS 2: Process all JavaScript files in the project. */
		// '../../**/*.js',

		/**
		 * Python: If you use Tailwind CSS classes in Python, uncomment the following line
		 * and make sure the pattern below matches your project structure.
		 */
		// '../../**/*.py'
	],
	theme: {
		extend: {
			fontFamily: {
				heading: ["Playfair Display"],
				sans: ["Inter"],
				roman: ["Times New Roman"],
			},
			colors: {
				white: "#F6F4F0",
				tan: "#EAE5DD",
				black: "#15130F",
				"light-gray": "#C4C1BB",
				gray: "#989691",
				"dark-gray": "#5B5C62",
				"dark-brown": "#443827",
				brown: "#8A614F",
			},
		},
	},
	plugins: [
		/**
		 * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
		 * for forms. If you don't like it or have own styling for forms,
		 * comment the line below to disable '@tailwindcss/forms'.
		 */
		require("@tailwindcss/forms"),
		require("@tailwindcss/typography"),
		require("@tailwindcss/line-clamp"),
		require("@tailwindcss/aspect-ratio"),
	],
};
