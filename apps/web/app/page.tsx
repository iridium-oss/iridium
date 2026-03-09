import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { BackToTop } from "@/components/layout/BackToTop";
import { Wuf13Strip } from "@/components/landing/Wuf13Strip";
import { Hero } from "@/components/landing/Hero";
import { Vision } from "@/components/landing/Vision";
import { Wuf13ContextSection } from "@/components/landing/Wuf13ContextSection";
import { WhyNow } from "@/components/landing/WhyNow";
import { Wuf13WhyIridiumSection } from "@/components/landing/Wuf13WhyIridiumSection";
import { Problem } from "@/components/landing/Problem";
import { Wuf13ThemeAlignment } from "@/components/landing/Wuf13ThemeAlignment";
import { MarketContext } from "@/components/landing/MarketContext";
import { GubaPlanSection } from "@/components/landing/GubaPlanSection";
import { UrbanMobilityByNumbers } from "@/components/landing/UrbanMobilityByNumbers";
import { WhyNowForBaku } from "@/components/landing/WhyNowForBaku";
import { Product } from "@/components/landing/Product";
import { HowItWorks } from "@/components/landing/HowItWorks";
import { RealDataTrust } from "@/components/landing/RealDataTrust";
import { KeyModules } from "@/components/landing/KeyModules";
import { UserValueProposition } from "@/components/landing/UserValueProposition";
import { InstitutionalValueProposition } from "@/components/landing/InstitutionalValueProposition";
import { BusinessModel } from "@/components/landing/BusinessModel";
import { GoToMarket } from "@/components/landing/GoToMarket";
import { Traction } from "@/components/landing/Traction";
import { Wuf13RelevanceMatrix } from "@/components/landing/Wuf13RelevanceMatrix";
import { CompetitiveLandscape } from "@/components/landing/CompetitiveLandscape";
import { WhyIridiumWins } from "@/components/landing/WhyIridiumWins";
import { TechnologyMoat } from "@/components/landing/TechnologyMoat";
import { DataMoat } from "@/components/landing/DataMoat";
import { Roadmap } from "@/components/landing/Roadmap";
import { RoadToWuf13 } from "@/components/landing/RoadToWuf13";
import { Team } from "@/components/landing/Team";
import { ResearchPublicationReadiness } from "@/components/landing/ResearchPublicationReadiness";
import { Wuf13CtaSection } from "@/components/landing/Wuf13CtaSection";
import { DemoCta } from "@/components/landing/DemoCta";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white pt-14">
      <Navbar />
      <Wuf13Strip />
      <main id="main-content" tabIndex={-1}>
        <Hero />
        <Vision />
        <Wuf13ContextSection />
        <WhyNow />
        <Wuf13WhyIridiumSection />
        <Problem />
        <Wuf13ThemeAlignment />
        <MarketContext />
        <GubaPlanSection />
        <UrbanMobilityByNumbers />
        <WhyNowForBaku />
        <Product />
        <HowItWorks />
        <RealDataTrust />
        <KeyModules />
        <UserValueProposition />
        <InstitutionalValueProposition />
        <BusinessModel />
        <GoToMarket />
        <Traction />
        <Wuf13RelevanceMatrix />
        <CompetitiveLandscape />
        <WhyIridiumWins />
        <TechnologyMoat />
        <DataMoat />
        <Roadmap />
        <RoadToWuf13 />
        <Team />
        <ResearchPublicationReadiness />
        <Wuf13CtaSection />
        <DemoCta />
      </main>
      <Footer />
      <BackToTop />
    </div>
  );
}
