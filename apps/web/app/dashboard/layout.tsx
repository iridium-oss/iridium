import { Navbar } from "@/components/layout/Navbar";
import { DashboardNav } from "@/components/dashboard/DashboardNav";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-surface-deepest">
      <Navbar />
      <div className="flex pt-16">
        <aside className="fixed left-0 top-16 z-40 h-[calc(100vh-4rem)] w-56 border-r border-surface-border bg-midnight-black/95 backdrop-blur md:w-64">
          <DashboardNav />
        </aside>
        <main className="flex-1 pl-56 md:pl-64">
          <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
