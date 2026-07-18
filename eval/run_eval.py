#!/usr/bin/env python3
"""
Northern Shift Guard — Evaluation runner.

Compares global-rule baseline (B1) vs zone-aware pipeline (B4) on labeled dataset.
Generates JSON report for paper tables.

Usage:
    cd eval
    python run_eval.py
    python run_eval.py --output results/report.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from baselines.global_rules import evaluate_global
from baselines.zone_aware import evaluate_zone_aware
from metrics.report import EvalReport, PPEMetrics

EVAL_DIR = Path(__file__).resolve().parent
LABELS_PATH = EVAL_DIR / "dataset" / "labels.json"
DEFAULT_OUTPUT = EVAL_DIR / "results" / "report.json"

# Zones where hard hat is NOT required — key for zone-flip / false alarm analysis
SURFACE_ZONE = "surface"
ACTIVE_ZONE = "active_stope"


def _update_ppe_metrics(metrics: PPEMetrics, predicted: str, actual: str) -> None:
    """Binary pass/fail update (treat unclear as fail for conservative eval)."""
    pred_pass = predicted == "pass"
    actual_pass = actual == "pass"
    if pred_pass and actual_pass:
        metrics.true_positives += 1
    elif pred_pass and not actual_pass:
        metrics.false_positives += 1
    elif not pred_pass and actual_pass:
        metrics.false_negatives += 1
    else:
        metrics.true_negatives += 1


def run_evaluation(labels_path: Path) -> EvalReport:
    data = json.loads(labels_path.read_text())
    report = EvalReport()

    for entry in data["images"]:
        report.total_images += 1
        hard_hat = entry["hard_hat"]
        hi_vis = entry["hi_vis"]
        gt = entry["ground_truth_compliance"]

        # PPE detection metrics (using ground-truth labels as perfect detector for now)
        _update_ppe_metrics(report.hard_hat_metrics, hard_hat, entry["hard_hat"])
        _update_ppe_metrics(report.hi_vis_metrics, hi_vis, entry["hi_vis"])

        # False alarm analysis on surface zone
        surface_gt_compliant = gt.get(SURFACE_ZONE) == "compliant"
        global_result = evaluate_global(hard_hat, hi_vis, surface_gt_compliant)
        zone_result = evaluate_zone_aware(hard_hat, hi_vis, SURFACE_ZONE, surface_gt_compliant)

        if global_result.false_alarm:
            report.global_false_alarms += 1
        if zone_result.false_alarm:
            report.zone_aware_false_alarms += 1

        # Zone-flip cases: surface compliant but active stope non-compliant
        if entry.get("zone_flip_case"):
            report.zone_flip_cases += 1
            surface_ok = evaluate_zone_aware(hard_hat, hi_vis, SURFACE_ZONE, True)
            active_gt = gt.get(ACTIVE_ZONE) == "compliant"
            active_ok = evaluate_zone_aware(hard_hat, hi_vis, ACTIVE_ZONE, active_gt)
            # Correct if surface doesn't false-alarm AND active stope catches violation
            if not surface_ok.false_alarm and active_ok.overall == gt.get(ACTIVE_ZONE):
                report.zone_flip_correct += 1

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Northern Shift Guard evaluation")
    parser.add_argument("--labels", type=Path, default=LABELS_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = run_evaluation(args.labels)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report.to_dict(), indent=2))

    print("Northern Shift Guard — Evaluation Report")
    print("=" * 45)
    d = report.to_dict()
    for key, val in d.items():
        if isinstance(val, dict):
            print(f"  {key}:")
            for k, v in val.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {val}")
    print(f"\nReport saved to {args.output}")


if __name__ == "__main__":
    main()
