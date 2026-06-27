import { useCallback, useEffect, useState } from "react";
import { ClipboardList, HardHat, ShieldCheck } from "lucide-react";
import { analyzeImage, fetchScans, fetchZones } from "./api";
import AppShell from "./components/AppShell";
import AnalysisResult from "./components/AnalysisResult";
import ImageUpload from "./components/ImageUpload";
import ScanHistory from "./components/ScanHistory";
import type { AnalyzeResponse, ScanSummary, ZoneDefinition } from "./types";

type Tab = "scan" | "history";

export default function App() {
  const [tab, setTab] = useState<Tab>("scan");
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [scans, setScans] = useState<ScanSummary[]>([]);
  const [zones, setZones] = useState<Record<string, ZoneDefinition>>({});

  const refreshScans = useCallback(async () => {
    setHistoryLoading(true);
    try {
      setScans(await fetchScans());
    } catch {
      setScans([]);
    } finally {
      setHistoryLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshScans();
    fetchZones().then(setZones).catch(() => {});
  }, [refreshScans]);

  async function handleAnalyze(file: File, zone: string) {
    setLoading(true);
    setError(null);
    try {
      const response = await analyzeImage(file, zone);
      setResult(response);
      await refreshScans();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error");
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell tab={tab} onTabChange={setTab}>
      {tab === "scan" ? (
        <div className="space-y-10">
          <section className="rounded-2xl border border-border bg-surface p-8 md:p-10">
            <p className="font-mono text-xs uppercase tracking-widest text-primary">
              Northern Ontario mining safety
            </p>
            <h1 className="mt-3 max-w-3xl text-4xl font-semibold leading-tight md:text-5xl">
              Catch the missing hard hat
              <span className="text-primary"> before the cage drops.</span>
            </h1>
            <p className="mt-4 max-w-2xl text-lg text-muted-foreground">
              Explainable AI shift-start screening: vision detects PPE and fatigue cues, Nemotron
              recommends zone-tailored supervisor actions, and every scan is stored in the audit log.
            </p>
            <div className="mt-8 grid gap-4 md:grid-cols-3">
              <Feature
                icon={<ClipboardList className="h-5 w-5" />}
                title="Zone-aware PPE check"
                body="PPE requirements checked against the specific mine zone — surface, pit, underground, and more."
              />
              <Feature
                icon={<ShieldCheck className="h-5 w-5" />}
                title="Fatigue screening"
                body="Visible fatigue cues flagged as a screening aid — not medical diagnosis."
              />
              <Feature
                icon={<HardHat className="h-5 w-5" />}
                title="Auditable trail"
                body="Evidence JSON, zone compliance, Nemotron action, and timestamp stored for every scan."
              />
            </div>
          </section>

          {error && (
            <div className="rounded-xl border border-fail/40 bg-fail/10 px-4 py-3 text-fail-foreground">
              <strong>Error:</strong> {error}
              <p className="mt-1 text-sm opacity-90">Make sure the backend is running on port 8000.</p>
            </div>
          )}

          <div className="grid gap-8 lg:grid-cols-2">
            <ImageUpload onAnalyze={handleAnalyze} loading={loading} zones={zones} />
            <AnalysisResult result={result} loading={loading} />
          </div>
        </div>
      ) : (
        <ScanHistory scans={scans} loading={historyLoading} onRefresh={refreshScans} />
      )}
    </AppShell>
  );
}

function Feature({
  icon,
  title,
  body,
}: {
  icon: React.ReactNode;
  title: string;
  body: string;
}) {
  return (
    <div className="rounded-xl border border-border bg-card p-4">
      <div className="flex h-9 w-9 items-center justify-center rounded-md bg-primary/15 text-primary">
        {icon}
      </div>
      <h3 className="mt-3 font-semibold">{title}</h3>
      <p className="mt-1 text-sm text-muted-foreground">{body}</p>
    </div>
  );
}
