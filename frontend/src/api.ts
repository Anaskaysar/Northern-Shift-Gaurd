import type { AnalyzeResponse, ScanSummary, ZoneDefinition } from "./types";

const API_BASE = (import.meta.env.VITE_API_BASE_URL ?? "").replace(/\/$/, "");

function apiUrl(path: string): string {
  return `${API_BASE}${path}`;
}

async function parseJsonResponse<T>(response: Response, fallbackError: string): Promise<T> {
  const text = await response.text();
  if (!response.ok) {
    throw new Error(text || `${fallbackError} (${response.status})`);
  }
  if (!text.trim()) {
    throw new Error(
      "Empty response from API. Deploy the Docker web service (not a static site) so the backend is available.",
    );
  }
  try {
    return JSON.parse(text) as T;
  } catch {
    throw new Error(
      "API returned a non-JSON response. Deploy as a Docker web service, not a Render static site.",
    );
  }
}

export async function analyzeImage(file: File, zone: string): Promise<AnalyzeResponse> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("zone", zone);

  const response = await fetch(apiUrl("/api/analyze"), {
    method: "POST",
    body: formData,
  });

  return parseJsonResponse(response, "Analysis failed");
}

export async function fetchScans(): Promise<ScanSummary[]> {
  const response = await fetch(apiUrl("/api/scans"));
  return parseJsonResponse(response, "Failed to load scan history");
}

export async function fetchZones(): Promise<Record<string, ZoneDefinition>> {
  const response = await fetch(apiUrl("/api/zones"));
  return parseJsonResponse(response, "Failed to load zones");
}
