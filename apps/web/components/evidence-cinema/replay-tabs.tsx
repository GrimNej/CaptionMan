"use client";

import { useState } from "react";
import type { JudgeReplayArtifact } from "@/lib/schemas";
import { CaptionCourtRail } from "./caption-court-rail";
import { EvidenceReel } from "./evidence-reel";
import { FinalCaptionCard } from "./final-caption-card";
import { TemporalEvidenceFile } from "./temporal-evidence-file";
import { VerdictExportPanel } from "./verdict-export-panel";

const tabs = ["Overview", "Evidence", "Court", "Verdict", "Raw JSON"] as const;

export function ReplayTabs({ artifact }: { artifact: JudgeReplayArtifact }) {
  const [active, setActive] = useState<(typeof tabs)[number]>("Overview");
  const officialJson = JSON.stringify(
    [{ task_id: artifact.video.id, captions: artifact.finalCaptions }],
    null,
    2,
  );

  return (
    <section className="grid gap-5">
      <div
        aria-label="Judge Verdict sections"
        className="cm-tabs"
        role="tablist"
      >
        {tabs.map((tab) => (
          <button
            aria-selected={active === tab}
            className="cm-tab"
            key={tab}
            onClick={() => setActive(tab)}
            role="tab"
            type="button"
          >
            {tab}
          </button>
        ))}
      </div>
      {active === "Overview" ? (
        <div className="grid gap-5">
          <EvidenceReel artifact={artifact} />
          <div className="cm-replay-grid">
            <TemporalEvidenceFile artifact={artifact} />
            <div className="grid gap-5">
              <FinalCaptionCard artifact={artifact} featured style="formal" />
            </div>
          </div>
        </div>
      ) : null}
      {active === "Evidence" ? (
        <div className="grid gap-5">
          <EvidenceReel artifact={artifact} />
          <TemporalEvidenceFile artifact={artifact} />
        </div>
      ) : null}
      {active === "Court" ? <CaptionCourtRail artifact={artifact} /> : null}
      {active === "Verdict" ? <VerdictExportPanel artifact={artifact} /> : null}
      {active === "Raw JSON" ? (
        <pre className="cm-json">{officialJson}</pre>
      ) : null}
    </section>
  );
}
