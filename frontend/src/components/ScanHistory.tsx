import { RefreshCw } from "lucide-react";
import type { ScanSummary } from "../types";
import { DecisionBadge } from "./DecisionBadge";
import { Button } from "@/components/ui/button";
import { decisionFromScan, priorityLabel } from "@/lib/status";

interface Props {
  scans: ScanSummary[];
  loading: boolean;
  onRefresh: () => void;
}

export default function ScanHistory({ scans, loading, onRefresh }: Props) {
  return (
    <section className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="font-mono text-xs uppercase tracking-widest text-muted-foreground">
            SQLite audit log
          </p>
          <h2 className="mt-1 text-3xl font-semibold">Scan history</h2>
        </div>
        <Button variant="outline" onClick={onRefresh} disabled={loading}>
          <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
          Refresh
        </Button>
      </div>

      {loading && scans.length === 0 ? (
        <div className="rounded-xl border border-border bg-card p-8 text-center text-muted-foreground">
          Loading audit trail…
        </div>
      ) : scans.length === 0 ? (
        <div className="rounded-xl border border-border bg-card p-8 text-center text-muted-foreground">
          No scans recorded yet. Run an AI scan to start building the audit trail.
        </div>
      ) : (
        <div className="overflow-hidden rounded-xl border border-border">
          <table className="w-full">
            <thead className="bg-surface text-left text-xs uppercase tracking-wider text-muted-foreground">
              <tr>
                <th className="px-4 py-3 font-medium">Scan</th>
                <th className="px-4 py-3 font-medium">PPE</th>
                <th className="px-4 py-3 font-medium">Fatigue</th>
                <th className="px-4 py-3 font-medium">Decision</th>
                <th className="px-4 py-3 font-medium">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {scans.map((scan) => (
                <tr key={scan.id} className="bg-card">
                  <td className="px-4 py-4 align-top">
                    <div className="font-mono text-sm">#{scan.id}</div>
                    <div className="mt-1 text-sm">{scan.image_filename}</div>
                    <div className="mt-1 font-mono text-xs text-muted-foreground">
                      {scan.created_at.replace("T", " ").slice(0, 19)} UTC
                    </div>
                  </td>
                  <td className="px-4 py-4 align-top text-sm">
                    <div>Hard hat: {scan.hard_hat}</div>
                    <div className="mt-1">Hi-vis: {scan.hi_vis}</div>
                  </td>
                  <td className="px-4 py-4 align-top text-sm uppercase">{scan.fatigue_risk}</td>
                  <td className="px-4 py-4 align-top">
                    <DecisionBadge
                      decision={decisionFromScan(scan.priority, scan.hard_hat, scan.hi_vis)}
                    />
                    <div className="mt-2 font-mono text-xs uppercase text-muted-foreground">
                      {priorityLabel(scan.priority)}
                    </div>
                  </td>
                  <td className="px-4 py-4 align-top text-sm text-muted-foreground">
                    {scan.supervisor_action}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
