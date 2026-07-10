"use client";

import { AlertTriangle, CheckCircle2 } from "lucide-react";
import { useState } from "react";
import type { CaptionStyle, JudgeReplayArtifact } from "@/lib/schemas";
import { styleLabels } from "./final-caption-card";
import { RepairDiff } from "./repair-diff";

const styles: CaptionStyle[] = [
  "formal",
  "sarcastic",
  "humorous_tech",
  "humorous_non_tech",
];

export function CaptionCourtRail({
  artifact,
}: {
  artifact: JudgeReplayArtifact;
}) {
  const [activeStyle, setActiveStyle] = useState<CaptionStyle>("formal");
  const active =
    artifact.court.find((item) => item.style === activeStyle) ??
    artifact.court[0];
  const flagged =
    active.candidates.find(
      (candidate) => candidate.unsupportedTerms.length > 0,
    ) ?? active.candidates.find((candidate) => !candidate.selected);

  return (
    <aside className="grid gap-5">
      <section className="cm-panel p-5">
        <div className="mb-5">
          <span className="cm-kicker">Caption Court</span>
          <h2 className="mt-2 text-2xl font-semibold">
            How each caption was challenged
          </h2>
        </div>
        <div
          aria-label="Caption style selector"
          className="cm-tabs"
          role="tablist"
        >
          {styles.map((style) => (
            <button
              aria-selected={activeStyle === style}
              className="cm-tab"
              key={style}
              onClick={() => setActiveStyle(style)}
              role="tab"
              type="button"
            >
              {styleLabels[style]}
            </button>
          ))}
        </div>
        <div className="grid gap-3">
          {active.candidates.map((candidate) => (
            <button
              aria-current={candidate.selected}
              className="cm-court-card"
              key={candidate.id}
              type="button"
            >
              <div className="mb-3 flex items-center justify-between gap-3">
                <span
                  className={
                    candidate.selected ? "cm-chip cm-chip-gold" : "cm-chip"
                  }
                >
                  {candidate.selected ? (
                    <CheckCircle2 size={14} />
                  ) : (
                    <AlertTriangle size={14} />
                  )}
                  {candidate.selected ? "Selected" : "Challenged"}
                </span>
                <span className={`cm-chip cm-risk-${candidate.risk}`}>
                  Risk: {candidate.risk}
                </span>
              </div>
              <p className="text-base leading-relaxed">{candidate.caption}</p>
              {candidate.unsupportedTerms.length > 0 ? (
                <div className="mt-3 flex flex-wrap gap-2">
                  {candidate.unsupportedTerms.map((term) => (
                    <span className="cm-chip cm-chip-ruby" key={term}>
                      Flag: {term}
                    </span>
                  ))}
                </div>
              ) : null}
              <div className="cm-score-grid mt-4">
                <div className="cm-score">
                  <span>Factuality</span>
                  <strong>{Math.round(candidate.factuality * 100)}%</strong>
                </div>
                <div className="cm-score">
                  <span>Tone</span>
                  <strong>{Math.round(candidate.tone * 100)}%</strong>
                </div>
                <div className="cm-score">
                  <span>Coverage</span>
                  <strong>{Math.round((1 - candidate.omission) * 100)}%</strong>
                </div>
              </div>
            </button>
          ))}
        </div>
      </section>
      {active.repair && flagged ? (
        <RepairDiff
          after={active.repair.after}
          before={active.repair.before}
          reasons={active.repair.reasons}
          unsupportedTerms={flagged.unsupportedTerms}
        />
      ) : null}
    </aside>
  );
}
