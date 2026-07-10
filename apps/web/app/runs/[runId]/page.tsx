import { AlertTriangle, Clock, Film, ShieldCheck } from "lucide-react";
import Link from "next/link";
import { CaptionCourtRail } from "@/components/evidence-cinema/caption-court-rail";
import { EvidenceReel } from "@/components/evidence-cinema/evidence-reel";
import { FinalCaptionCard } from "@/components/evidence-cinema/final-caption-card";
import { ProviderStatusMini } from "@/components/evidence-cinema/provider-status-mini";
import { ReplayTabs } from "@/components/evidence-cinema/replay-tabs";
import { SignatureMomentStrip } from "@/components/evidence-cinema/signature-moment-strip";
import { SubmissionReadinessStrip } from "@/components/evidence-cinema/submission-readiness-strip";
import { TemporalEvidenceFile } from "@/components/evidence-cinema/temporal-evidence-file";
import { Shell } from "@/components/layout/shell";
import { getReplayArtifact } from "@/lib/replay-artifact";

export default async function JudgeReplayPage({
  params,
}: {
  params: Promise<{ runId: string }>;
}) {
  const { runId } = await params;
  const artifactResult = await getReplayArtifact(runId)
    .then((artifact) => ({ artifact, error: "" }))
    .catch((error) => ({
      artifact: null,
      error:
        error instanceof Error
          ? error.message
          : "Could not load this Judge Verdict.",
    }));

  if (!artifactResult.artifact) {
    return (
      <Shell>
        <main className="cm-page grid gap-7">
          <section className="cm-panel p-8">
            <span className="cm-kicker">
              <AlertTriangle size={15} />
              Judge Verdict / {runId}
            </span>
            <h1 className="mt-4 max-w-3xl text-4xl font-semibold leading-none md:text-6xl">
              This verdict could not be loaded.
            </h1>
            <p className="cm-muted mt-4 max-w-2xl">
              {artifactResult.error} Return to the Studio and open the verdict
              from a completed run.
            </p>
            <Link className="cm-button cm-button-primary mt-6" href="/studio">
              Back to Studio
            </Link>
          </section>
        </main>
      </Shell>
    );
  }

  const artifact = artifactResult.artifact;

  return (
    <Shell>
      <main className="cm-page grid gap-7">
        <section className="cm-replay-grid">
          <div className="grid gap-5">
            <div className="cm-cinema-frame">
              <div className="cm-video-meta">
                <div>
                  <span className="cm-kicker">
                    <Film size={15} />
                    Judge Verdict / {artifact.runId}
                  </span>
                  <h1 className="mt-3 max-w-2xl text-4xl font-semibold leading-none md:text-6xl">
                    Evidence, challenges, and final captions in one place.
                  </h1>
                </div>
                <div className="grid gap-2">
                  <span className="cm-chip cm-chip-gold">
                    <Clock size={14} />
                    {artifact.video.durationSec}s
                  </span>
                  <span className="cm-chip">
                    <ShieldCheck size={14} />
                    Evidence-backed caption export
                  </span>
                </div>
              </div>
            </div>
            <ProviderStatusMini compact />
            <SignatureMomentStrip artifact={artifact} />
            <EvidenceReel artifact={artifact} />
            <TemporalEvidenceFile artifact={artifact} />
          </div>
          <div className="grid gap-5">
            <CaptionCourtRail artifact={artifact} />
            <FinalCaptionCard artifact={artifact} featured style="formal" />
          </div>
        </section>
        <ReplayTabs artifact={artifact} />
        <SubmissionReadinessStrip />
      </main>
    </Shell>
  );
}
