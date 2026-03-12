import type { Metadata } from "next";
// import "@fontsource-variable/google-sans";
 import "./globals.css";
import { DisclaimerBanner } from "@/components/layout/DisclaimerBanner";
import { SkipLink } from "@/components/layout/SkipLink";

export const metadata: Metadata = {
  title: "IRIDIUM - Real-time urban mobility prediction and optimization",
  description:
    "Provenance-aware real-data urban mobility platform for Azerbaijani cities. Digital twin, federated learning, multimodal routing, equity analytics, anomaly detection.",
  keywords: ["urban mobility", "digital twin", "Baku", "Guba", "Azerbaijan", "WUF13", "transit", "routing", "provenance"],
  openGraph: {
    title: "IRIDIUM - Urban Mobility Intelligence",
    description: "Provenance-aware digital twin platform for Azerbaijani cities. Real-time, source-labeled city intelligence.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    
    <html lang="en">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen bg-[var(--surface-deepest)] text-text-primary font-sans antialiased">
        <SkipLink />
        <DisclaimerBanner />
        {children}
      </body>
    </html>
  );
}
