"use client";

import { Check, Copy } from "lucide-react";
import { useState } from "react";
import type { CaptionStyle, JudgeReplayArtifact } from "@/lib/schemas";
import { VerdictStamp } from "./verdict-stamp";

const styleLabels: Record<CaptionStyle, string> = {
  formal: "Formal",
  sarcastic: "Sarcastic",
  humorous_tech: "Humorous Tech",
  humorous_non_tech: "Humorous Non-Tech",
};

function selectedCandidate(artifact: JudgeReplayArtifact, style: CaptionStyle) {
  return artifact.court
    .find((item) => item.style === style)
    ?.candidates.find((item) => item.selected);
}

export function FinalCaptionCard({
  artifact,
  style,
  featured = false,
}: {
  artifact: JudgeReplayArtifact;
  style: CaptionStyle;
  featured?: boolean;
}) {
  const [copied, setCopied] = useState(false);
  const caption = artifact.finalCaptions[style];
  const candidate = selectedCandidate(artifact, style);

  return (
    <article
      className={`cm-final-card ${featured ? "cm-final-card-selected" : ""}`}
    >
      {featured ? <VerdictStamp /> : null}
      <div className="mb-8 flex items-start justify-between gap-4">
        <div>
          <span className="cm-kicker">{styleLabels[style]}</span>
          <p className="cm-muted mt-2 text-sm">
            Selected caption with receipt-backed verdict
          </p>
        </div>
        <button
          aria-label={`Copy ${styleLabels[style]} caption`}
          className="cm-button"
          onClick={async () => {
            await navigator.clipboard.writeText(caption);
            setCopied(true);
            window.setTimeout(() => setCopied(false), 1200);
          }}
          type="button"
        >
          {copied ? <Check size={16} /> : <Copy size={16} />}
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <p className="cm-caption-text max-w-2xl">{caption}</p>
      <div className="cm-score-grid mt-7">
        <div className="cm-score">
          <span>Factuality</span>
          <strong>{Math.round((candidate?.factuality ?? 0.9) * 100)}%</strong>
        </div>
        <div className="cm-score">
          <span>Tone</span>
          <strong>{Math.round((candidate?.tone ?? 0.9) * 100)}%</strong>
        </div>
        <div className="cm-score">
          <span>Risk</span>
          <strong className={`cm-risk-${candidate?.risk ?? "low"}`}>
            {candidate?.risk ?? "low"}
          </strong>
        </div>
      </div>
    </article>
  );
}

export { styleLabels };
