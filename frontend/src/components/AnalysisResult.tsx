import { AlertTriangle, Brain, Eye, HardHat, MapPin, ShieldCheck } from "lucide-react";
import type { AnalyzeResponse } from "../types";
import { DecisionBadge, StatusPill } from "./DecisionBadge";
import {
  computeOverallDecision,
  fatigueTone,
  ppeStatusLabel,
  ppeStatusTone,
  priorityLabel,
} from "@/lib/status";

interface Props {
  result: AnalyzeResponse | null;
  loading: boolean;
}

export default function AnalysisResult({ result, loading }: Props) {
  if (loading) {
    return (
      <section className="rounded-xl border border-border bg-card p-8">
        <div className="flex flex-col items-center justify-center gap-4 py-16">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-border border-t-primary" />
          <p className="text-muted-foreground">Running vision + Nemotron analysis…</p>
        </div>
      </section>
    );
  }

  if (!result) {
    return (
      <section className="rounded-xl border border-border bg-card p-8">
        <div className="flex items-start gap-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-md bg-primary/15 text-primary">
            <ShieldCheck className="h-5 w-5" />
          </div>
          <div>
            <h3 className="text-lg font-semibold">Results will appear here</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              Upload a worker photo to see PPE compliance, fatigue screening, explainable evidence,
              and Nemotron&apos;s supervisor action.
            </p>
          </div>
        </div>
      </section>
    );
  }

  const { vision, nemotron, provider } = result;
  const overall = computeOverallDecision(result);

  return (
    <section className="space-y-4">
      <div className="rounded-xl border border-border bg-card p-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="font-mono text-xs uppercase tracking-widest text-muted-foreground">
              Scan #{result.scan_id}
            </p>
            <h3 className="mt-1 text-xl font-semibold">Analysis complete</h3>
          </div>
          <DecisionBadge decision={overall} />
        </div>
        <p className="mt-3 font-mono text-xs text-muted-foreground">
          vision:{provider.vision} · nemotron:{provider.nemotron}
        </p>
      </div>

      <div className="grid gap-3 md:grid-cols-3">
        <MetricCard
          icon={HardHat}
          label="Hard hat"
          value={ppeStatusLabel(vision.ppe.hard_hat)}
          tone={ppeStatusTone(vision.ppe.hard_hat)}
        />
        <MetricCard
          icon={ShieldCheck}
          label="Hi-vis vest"
          value={ppeStatusLabel(vision.ppe.hi_vis)}
          tone={ppeStatusTone(vision.ppe.hi_vis)}
        />
        <MetricCard
          icon={Eye}
          label="Fatigue risk"
          value={vision.fatigue.risk}
          tone={fatigueTone(vision.fatigue.risk)}
        />
      </div>

      {/* Zone compliance panel */}
      {result.zone_compliance && (
        <div className="rounded-xl border border-border bg-card p-6">
          <div className="flex items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <MapPin className="h-5 w-5 text-primary" />
              <h3 className="text-lg font-semibold">Zone compliance</h3>
            </div>
            <StatusPill
              label={result.zone_compliance.overall === "compliant" ? "Compliant" : "Non-compliant"}
              tone={result.zone_compliance.overall === "compliant" ? "pass" : "fail"}
            />
          </div>
          <p className="mt-1 text-sm text-muted-foreground">
            {result.zone_compliance.zone_name} · {result.zone_compliance.regulation}
          </p>
          <div className="mt-4 space-y-2">
            {result.zone_compliance.requirements.map((req) => (
              <div
                key={req.ppe_item}
                className="flex items-center justify-between rounded-lg border border-border bg-surface px-4 py-3 text-sm"
              >
                <div>
                  <span className="font-semibold">{req.label}</span>
                  <span className="ml-2 text-muted-foreground text-xs">
                    {req.required ? "Required" : "Not required"}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-muted-foreground uppercase">
                    detected: {req.detected}
                  </span>
                  <StatusPill
                    label={
                      req.compliant === "compliant"
                        ? "✓ OK"
                        : req.compliant === "not_required"
                        ? "—"
                        : "✗ Fail"
                    }
                    tone={
                      req.compliant === "compliant"
                        ? "pass"
                        : req.compliant === "not_required"
                        ? "pending"
                        : "fail"
                    }
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="rounded-xl border border-border bg-surface p-6">
        <div className="flex items-center gap-2 text-primary">
          <Brain className="h-5 w-5" />
          <h3 className="text-lg font-semibold">Supervisor action</h3>
          <StatusPill label={priorityLabel(nemotron.priority)} tone={overall === "pass" ? "pass" : overall === "conditional" ? "conditional" : "fail"} />
        </div>
        <p className="mt-4 text-base font-medium leading-relaxed">{nemotron.supervisor_action}</p>
        <p className="mt-3 text-sm text-muted-foreground">{nemotron.rationale}</p>
        {nemotron.recommended_steps.length > 0 && (
          <ul className="mt-4 space-y-2 text-sm">
            {nemotron.recommended_steps.map((step) => (
              <li key={step} className="flex gap-2">
                <span className="text-primary">•</span>
                <span>{step}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="rounded-xl border border-border bg-card p-6">
        <h3 className="text-lg font-semibold">Explainable evidence</h3>
        {vision.explanation && (
          <p className="mt-2 text-sm text-muted-foreground">{vision.explanation}</p>
        )}
        <ul className="mt-4 space-y-3">
          {vision.evidence.map((item) => (
            <li
              key={`${item.region}-${item.observation}`}
              className="rounded-lg border border-border bg-surface p-3 text-sm"
            >
              <div className="flex flex-wrap items-center gap-2">
                <strong>{item.region}</strong>
                <StatusPill
                  label={item.severity}
                  tone={
                    item.severity === "critical"
                      ? "fail"
                      : item.severity === "warning"
                        ? "conditional"
                        : "pass"
                  }
                />
              </div>
              <p className="mt-2">{item.observation}</p>
            </li>
          ))}
        </ul>
        {vision.fatigue.indicators.length > 0 && (
          <p className="mt-4 flex items-start gap-2 text-sm text-muted-foreground">
            <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-conditional" />
            Fatigue indicators: {vision.fatigue.indicators.join(", ")}
          </p>
        )}
      </div>
    </section>
  );
}

function MetricCard({
  icon: Icon,
  label,
  value,
  tone,
}: {
  icon: typeof HardHat;
  label: string;
  value: string;
  tone: "pass" | "conditional" | "fail" | "pending";
}) {
  return (
    <div className="rounded-xl border border-border bg-card p-4">
      <div className="flex items-center gap-2 text-muted-foreground">
        <Icon className="h-4 w-4" />
        <span className="text-sm">{label}</span>
      </div>
      <div className="mt-3 flex items-center justify-between gap-2">
        <span className="font-mono text-lg font-semibold uppercase">{value}</span>
        <StatusPill label={value} tone={tone} />
      </div>
    </div>
  );
}
