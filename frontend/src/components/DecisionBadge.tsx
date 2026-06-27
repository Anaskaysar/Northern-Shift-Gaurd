import { DECISION_META, type Decision } from "@/lib/status";
import { cn } from "@/lib/utils";

export function DecisionBadge({ decision }: { decision: Decision }) {
  const meta = DECISION_META[decision];
  const cls =
    meta.tone === "pass"
      ? "bg-pass text-pass-foreground"
      : meta.tone === "conditional"
        ? "bg-conditional text-conditional-foreground"
        : meta.tone === "fail"
          ? "bg-fail text-fail-foreground"
          : "bg-pending text-pending-foreground";

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md px-2.5 py-1 text-xs font-semibold uppercase tracking-wider",
        cls,
      )}
    >
      {meta.label}
    </span>
  );
}

export function StatusPill({
  label,
  tone,
}: {
  label: string;
  tone: "pass" | "conditional" | "fail" | "pending";
}) {
  const cls =
    tone === "pass"
      ? "bg-pass text-pass-foreground"
      : tone === "conditional"
        ? "bg-conditional text-conditional-foreground"
        : tone === "fail"
          ? "bg-fail text-fail-foreground"
          : "bg-pending text-pending-foreground";

  return (
    <span className={cn("inline-flex rounded-md px-2 py-0.5 text-xs font-semibold uppercase", cls)}>
      {label}
    </span>
  );
}
