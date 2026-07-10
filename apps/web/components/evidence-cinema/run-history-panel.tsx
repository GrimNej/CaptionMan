import {
  CheckCircle2,
  Clock3,
  ExternalLink,
  History,
  RotateCcw,
  XCircle,
} from "lucide-react";
import Link from "next/link";

type ApiRun = {
  run_id?: string;
  status?: string;
  error?: string;
};

async function getRuns(): Promise<ApiRun[]> {
  try {
    const base =
      process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
    const response = await fetch(`${base}/api/runs`, { cache: "no-store" });
    if (!response.ok) {
      return [];
    }
    const data = await response.json();
    return Array.isArray(data) ? data : [];
  } catch {
    return [];
  }
}

export async function RunHistoryPanel() {
  const runs = (await getRuns())
    .filter((run) => run.run_id)
    .sort((a, b) => String(b.run_id).localeCompare(String(a.run_id)))
    .slice(0, 6);

  return (
    <div className="cm-panel p-6">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <span className="cm-kicker">
          <History size={15} />
          Recent runs
        </span>
        <span className="cm-chip">
          <RotateCcw size={14} />
          Live API
        </span>
      </div>
      {runs.length > 0 ? (
        <div className="grid gap-3">
          {runs.map((run) => (
            <Link
              className="cm-run-row cm-panel-soft flex items-center justify-between gap-3 p-3"
              href={`/runs/${run.run_id}`}
              key={run.run_id}
              prefetch={false}
            >
              <span className="min-w-0">
                <strong className="block truncate">{run.run_id}</strong>
                <span className="cm-muted text-sm">Open Judge Verdict</span>
              </span>
              <span className="flex shrink-0 items-center gap-2">
                <StatusChip status={run.status} />
                <ExternalLink color="var(--cm-evidence-gold)" size={16} />
              </span>
            </Link>
          ))}
        </div>
      ) : (
        <div className="cm-panel-soft p-4">
          <p className="font-semibold">No completed API runs yet.</p>
          <p className="cm-muted mt-2 text-sm">
            Paste a direct video URL or upload a file, run it, then open the
            completed Judge Verdict from the result panel.
          </p>
        </div>
      )}
    </div>
  );
}

function StatusChip({ status }: { status?: string }) {
  if (status === "complete") {
    return (
      <span className="cm-chip cm-chip-teal">
        <CheckCircle2 size={14} />
        Complete
      </span>
    );
  }
  if (status === "failed") {
    return (
      <span className="cm-chip cm-chip-ruby">
        <XCircle size={14} />
        Failed
      </span>
    );
  }
  return (
    <span className="cm-chip">
      <Clock3 size={14} />
      {status ?? "Unknown"}
    </span>
  );
}
