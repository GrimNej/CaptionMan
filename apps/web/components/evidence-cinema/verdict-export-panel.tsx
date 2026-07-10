"use client";

import { Download, FileJson, ScrollText } from "lucide-react";
import { useMemo } from "react";
import type { JudgeReplayArtifact } from "@/lib/schemas";
import { FinalCaptionCard } from "./final-caption-card";

export function VerdictExportPanel({
  artifact,
}: {
  artifact: JudgeReplayArtifact;
}) {
  const officialJson = useMemo(
    () => [
      {
        task_id: artifact.video.id,
        captions: artifact.finalCaptions,
      },
    ],
    [artifact],
  );
  const json = JSON.stringify(officialJson, null, 2);

  return (
    <section className="grid gap-5">
      <div className="cm-panel p-5">
        <div className="mb-5 flex flex-wrap items-start justify-between gap-4">
          <div>
            <span className="cm-kicker">Verdict Export</span>
            <h2 className="mt-2 text-2xl font-semibold">
              Final captions and official JSON
            </h2>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              className="cm-button"
              onClick={() => navigator.clipboard.writeText(json)}
              type="button"
            >
              <FileJson size={16} />
              Copy JSON
            </button>
            <a
              className="cm-button cm-button-primary"
              download="captionman-results.json"
              href={`data:application/json;charset=utf-8,${encodeURIComponent(json)}`}
            >
              <Download size={16} />
              Download
            </a>
          </div>
        </div>
        <div className="grid gap-4 lg:grid-cols-2">
          {(
            [
              "formal",
              "sarcastic",
              "humorous_tech",
              "humorous_non_tech",
            ] as const
          ).map((style) => (
            <FinalCaptionCard artifact={artifact} key={style} style={style} />
          ))}
        </div>
      </div>
      <div className="cm-panel p-5">
        <div className="mb-4 flex items-center gap-2">
          <ScrollText color="var(--cm-evidence-gold)" size={18} />
          <h3 className="text-lg font-semibold">Official output preview</h3>
        </div>
        <pre className="cm-json">{json}</pre>
      </div>
    </section>
  );
}
