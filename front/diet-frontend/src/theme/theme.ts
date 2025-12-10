export const theme = {
  colors: {
    background: "#f9fafb",
    primary: "#4f46e5",
    primarySoft: "#a5b4fc",
    accent: "#fb7185",
    accentSoft: "#ffe4e6",
    textMain: "#111827",
    textSub: "#6b7280",
    cardBg: "#ffffff",
    border: "#e5e7eb",
    
    bubbleBot: "#f3e8ff",       /* 🤖 봇 말풍선 색상 */
  

    bubbleUser: "#FFD6E7",      
    
    bubbleUserBorder: "#FFB6C1", 
    bubbleUserText: "#333333",
  },
  fontSizes: {
    xs: "11px",
    sm: "13px",
    md: "15px",
    lg: "18px",
    xl: "22px",
    title: "26px",
  },
  radii: {
    sm: "8px",
    md: "12px",
    lg: "18px",
    pill: "999px",
  },
  shadows: {
    soft: "0 8px 20px rgba(15, 23, 42, 0.12)",
  },
};
export type AppTheme = typeof theme;