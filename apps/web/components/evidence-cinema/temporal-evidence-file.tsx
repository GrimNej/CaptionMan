import type { JudgeReplayArtifact } from "@/lib/schemas";

export function TemporalEvidenceFile({
  artifact,
}: {
  artifact: JudgeReplayArtifact;
}) {
  return (
    <section className="cm-panel p-5">
      <div className="mb-5">
        <span className="cm-kicker">Temporal Evidence File</span>
        <h2 className="mt-2 text-2xl font-semibold">What the system saw</h2>
        <p className="cm-muted mt-2 text-sm">
          Structured evidence from sampled visual/audio cues.
        </p>
      </div>
      <div className="grid gap-3">
        {artifact.evidenceSegments.map((segment) => (
          <article className="cm-panel-soft p-4" key={segment.id}>
            <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
              <span className="cm-chip cm-chip-gold">
                {segment.id} | {segment.startSec.toFixed(1)}-
                {segment.endSec.toFixed(1)}s
              </span>
              <span className="cm-chip">
                Confidence {Math.round(segment.confidence * 100)}%
              </span>
            </div>
            <p className="text-lg leading-relaxed">{segment.summary}</p>
            <div className="mt-4 flex flex-wrap gap-2">
              {segment.supportedBy.map((frame) => (
                <span className="cm-chip cm-chip-gold" key={frame}>
                  Supported by {frame}
                </span>
              ))}
            </div>
            <div className="mt-3 flex flex-wrap gap-2">
              {segment.avoidClaims.map((claim) => (
                <span className="cm-chip cm-chip-ruby" key={claim}>
                  Avoid: {claim}
                </span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
