import { useRef, useState } from "react";
import { Upload, MapPin } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { ZoneDefinition } from "../types";

interface Props {
  onAnalyze: (file: File, zone: string) => void;
  loading: boolean;
  zones: Record<string, ZoneDefinition>;
}

const ZONE_ORDER = ["surface", "open_pit", "underground_entry", "active_stope", "processing_plant"];

export default function ImageUpload({ onAnalyze, loading, zones }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [dragging, setDragging] = useState(false);
  const [selectedZone, setSelectedZone] = useState("open_pit");

  function handleFile(file: File | undefined) {
    if (!file || !file.type.startsWith("image/")) return;
    setPreview(URL.createObjectURL(file));
    onAnalyze(file, selectedZone);
  }

  const zoneKeys = ZONE_ORDER.filter((k) => k in zones);

  return (
    <section className="space-y-4">
      <div>
        <p className="font-mono text-xs uppercase tracking-widest text-muted-foreground">
          Shift-start AI scan
        </p>
        <h2 className="mt-1 text-2xl font-semibold">Upload worker photo</h2>
        <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
          Vision model checks hard hat and hi-vis vest compliance, screens visible fatigue cues,
          and Nemotron recommends a prioritized supervisor action.
        </p>
      </div>

      {/* Zone selector */}
      <div className="rounded-xl border border-border bg-card p-4 space-y-3">
        <div className="flex items-center gap-2 text-sm font-semibold">
          <MapPin className="h-4 w-4 text-primary" />
          Select mine zone
        </div>
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
          {zoneKeys.map((key) => {
            const zone = zones[key];
            const active = selectedZone === key;
            return (
              <button
                key={key}
                onClick={() => setSelectedZone(key)}
                className={`rounded-lg border p-3 text-left text-sm transition-colors ${
                  active
                    ? "border-primary bg-primary/10 text-foreground"
                    : "border-border bg-surface text-muted-foreground hover:border-primary/50"
                }`}
              >
                <div className="font-semibold">{zone.name}</div>
                <div className="mt-0.5 text-xs opacity-75">{zone.description}</div>
                <div className="mt-1 text-xs font-mono opacity-60">
                  Requires: {zone.required_ppe.join(", ").replace(/_/g, " ")}
                </div>
              </button>
            );
          })}
        </div>
        {selectedZone && zones[selectedZone] && (
          <p className="text-xs text-muted-foreground font-mono">
            Regulation: {zones[selectedZone].regulation}
          </p>
        )}
      </div>

      {/* Drop zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => { e.preventDefault(); setDragging(false); handleFile(e.dataTransfer.files[0]); }}
        onClick={() => inputRef.current?.click()}
        className={`cursor-pointer rounded-xl border-2 border-dashed p-8 text-center transition-colors ${
          dragging ? "border-primary bg-primary/10" : "border-border bg-card hover:border-primary/60"
        }`}
      >
        {preview ? (
          <img
            src={preview}
            alt="Worker preview"
            className="mx-auto max-h-72 max-w-full rounded-lg object-contain"
          />
        ) : (
          <>
            <Upload className="mx-auto h-10 w-10 text-primary" />
            <p className="mt-4 font-semibold">Drop worker photo here</p>
            <p className="mt-1 text-sm text-muted-foreground">or click to browse · JPG, PNG, WEBP</p>
          </>
        )}
      </div>

      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        hidden
        onChange={(e) => handleFile(e.target.files?.[0])}
      />

      <div className="flex flex-wrap gap-3">
        <Button disabled={loading} onClick={() => inputRef.current?.click()} size="lg">
          {loading ? "Analyzing…" : "Choose image"}
        </Button>
        {preview && !loading && (
          <Button
            variant="outline"
            onClick={() => {
              setPreview(null);
              if (inputRef.current) inputRef.current.value = "";
            }}
          >
            Clear preview
          </Button>
        )}
      </div>

      <p className="text-sm text-muted-foreground">
        Fatigue output is a screening aid only — not a medical diagnosis.
      </p>
    </section>
  );
}
