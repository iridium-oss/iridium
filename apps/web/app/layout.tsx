import type { Metadata } from "next";
import "@fontsource-variable/google-sans";
import "./globals.css";
import { DisclaimerBanner } from "@/components/layout/DisclaimerBanner";

export const metadata: Metadata = {
  title: "IRIDIUM - Real-time urban mobility prediction and optimization",
  description:
    "Provenance-aware real-data urban mobility platform for Azerbaijani cities. Digital twin, federated learning, multimodal routing, equity analytics, anomaly detection.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen bg-surface-deepest text-text-primary font-sans antialiased">
        <DisclaimerBanner />
        {children}
      </body>
    </html>
  );
}
