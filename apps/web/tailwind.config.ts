import type { Config } from "tailwindcss";

export default {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-google-sans)", "system-ui", "sans-serif"],
      },
      colors: {
        midnight: {
          black: "#02010a",
          prussian: "#04052e",
          twilight: "#140152",
          navy: "#22007c",
          electric: "#0d00a4",
        },
        surface: {
          deepest: "var(--surface-deepest)",
          dark: "var(--surface-dark)",
          card: "var(--surface-card)",
          elevated: "var(--surface-elevated)",
          border: "var(--surface-border)",
        },
        accent: {
          luminous: "var(--accent-luminous)",
          focus: "var(--accent-focus)",
          muted: "var(--accent-muted)",
        },
        text: {
          primary: "var(--text-primary)",
          secondary: "var(--text-secondary)",
          muted: "var(--text-muted)",
        },
      },
      borderRadius: {
        xs: "var(--radius-xs)",
        sm: "var(--radius-sm)",
        md: "var(--radius-md)",
        lg: "var(--radius-lg)",
        xl: "var(--radius-xl)",
      },
      boxShadow: {
        glow: "0 0 24px var(--accent-glow)",
        card: "var(--shadow-card)",
        elevated: "var(--shadow-elevated)",
      },
      spacing: {
        4.5: "1.125rem",
        18: "4.5rem",
        22: "5.5rem",
      },
      animation: {
        "fade-in": "fadeIn 0.3s ease-out",
        "slide-up": "slideUp 0.35s ease-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
