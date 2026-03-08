import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Hero } from "@/components/landing/Hero";
import { WhatIridium } from "@/components/landing/WhatIridium";
import { WhyUrbanMobility } from "@/components/landing/WhyUrbanMobility";
import { CoreModules } from "@/components/landing/CoreModules";
import { RealDataTwin } from "@/components/landing/RealDataTwin";
import { FederatedPrivacy } from "@/components/landing/FederatedPrivacy";
import { MultimodalRouting } from "@/components/landing/MultimodalRouting";
import { EquityAnalytics } from "@/components/landing/EquityAnalytics";
import { AnomalyDetection } from "@/components/landing/AnomalyDetection";
import { LiveDemoCta } from "@/components/landing/LiveDemoCta";
import { TechnicalCredibility } from "@/components/landing/TechnicalCredibility";
import { ResearchPublication } from "@/components/landing/ResearchPublication";
import { OpenSourceInfra } from "@/components/landing/OpenSourceInfra";

export default function HomePage() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main>
        <Hero />
        <WhatIridium />
        <WhyUrbanMobility />
        <CoreModules />
        <RealDataTwin />
        <FederatedPrivacy />
        <MultimodalRouting />
        <EquityAnalytics />
        <AnomalyDetection />
        <LiveDemoCta />
        <TechnicalCredibility />
        <ResearchPublication />
        <OpenSourceInfra />
      </main>
      <Footer />
    </div>
  );
}
