import { HardHat, History, ScanLine } from "lucide-react";
import type { ReactNode } from "react";
import ThemeToggle from "./ThemeToggle";

type Tab = "scan" | "history";

interface Props {
  tab: Tab;
  onTabChange: (tab: Tab) => void;
  children: ReactNode;
}

export default function AppShell({ tab, onTabChange, children }: Props) {
  const nav: { id: Tab; label: string; icon: typeof ScanLine }[] = [
    { id: "scan", label: "AI scan", icon: ScanLine },
    { id: "history", label: "Audit trail", icon: History },
  ];

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-surface">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
          <div className="flex items-center gap-2 font-semibold">
            <HardHat className="h-5 w-5 text-primary" />
            <span>Northern Shift Guard</span>
          </div>

          <div className="flex items-center gap-2">
            <nav className="flex items-center gap-1">
              {nav.map((item) => {
                const Icon = item.icon;
                const active = tab === item.id;
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => onTabChange(item.id)}
                    className={`flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors ${
                      active
                        ? "bg-primary/15 text-primary"
                        : "text-muted-foreground hover:bg-accent hover:text-foreground"
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span className="hidden sm:inline">{item.label}</span>
                  </button>
                );
              })}
            </nav>
            <ThemeToggle />
          </div>

          <div className="hidden text-right md:block">
            <div className="text-sm font-medium leading-tight">NorthMind</div>
            <div className="font-mono text-xs uppercase text-muted-foreground">
              Mining &amp; Industrial Innovation
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
    </div>
  );
}
