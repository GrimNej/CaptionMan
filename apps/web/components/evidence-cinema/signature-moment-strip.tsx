import { AlertTriangle, CheckCircle2, Stamp } from "lucide-react";
import type { JudgeReplayArtifact } from "@/lib/schemas";

export function SignatureMomentStrip({
  artifact,
}: {
  artifact: JudgeReplayArtifact;
}) {
  const repaired = artifact.court.find((item) => item.repair)?.repair;

  return (
    <section
      aria-label="Signature repair to verdict moment"
      className="cm-panel p-4"
    >
      <div className="grid gap-3 md:grid-cols-3">
        <div className="cm-panel-soft p-4">
          <span className="cm-chip cm-chip-ruby">
            <AlertTriangle size={14} />
            Ruby flag
          </span>
          <p className="mt-3 text-lg font-semibold">
            <mark className="cm-mark-ruby">chef</mark> and{" "}
            <mark className="cm-mark-ruby">restaurant</mark> are unsupported.
          </p>
        </div>
        <div className="cm-panel-soft p-4">
          <span className="cm-chip cm-chip-gold">
            <CheckCircle2 size={14} />
            Repair diff
          </span>
          <p className="mt-3 text-lg font-semibold">
            {repaired?.after ??
              "A safer caption keeps only evidence-backed claims."}
          </p>
        </div>
        <div className="cm-panel-soft p-4">
          <span className="cm-chip cm-chip-gold">
            <Stamp size={14} />
            Gold verdict
          </span>
          <p className="mt-3 text-lg font-semibold">
            Final caption is stamped and exported with evidence receipts.
          </p>
        </div>
      </div>
    </section>
  );
}
