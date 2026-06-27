import type { AnalyzeResponse, ScanSummary, ZoneDefinition } from "./types";

export async function analyzeImage(file: File, zone: string): Promise<AnalyzeResponse> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("zone", zone);

  const response = await fetch("/api/analyze", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || "Analysis failed");
  }

  return response.json();
}

export async function fetchScans(): Promise<ScanSummary[]> {
  const response = await fetch("/api/scans");
  if (!response.ok) throw new Error("Failed to load scan history");
  return response.json();
}

export async function fetchZones(): Promise<Record<string, ZoneDefinition>> {
  const response = await fetch("/api/zones");
  if (!response.ok) throw new Error("Failed to load zones");
  return response.json();
}
