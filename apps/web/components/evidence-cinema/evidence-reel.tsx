"use client";

import { Film, ScanSearch } from "lucide-react";
import Image from "next/image";
import { useState } from "react";
import type { JudgeReplayArtifact } from "@/lib/schemas";

export function EvidenceReel({ artifact }: { artifact: JudgeReplayArtifact }) {
  const [selected, setSelected] = useState(0);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const selectedFrame = artifact.frames[selected];
  const supportedSegments = artifact.evidenceSegments.filter((segment) =>
    segment.supportedBy.includes(selectedFrame.id),
  );

  return (
    <section className="cm-panel p-5">
      <div className="mb-5 flex items-start justify-between gap-4">
        <div>
          <span className="cm-kicker">Evidence Reel</span>
          <h2 className="mt-2 text-2xl font-semibold">
            Frames become receipts
          </h2>
        </div>
        <span className="cm-chip cm-chip-gold">
          <Film size={14} />
          {artifact.frames.length} frames
        </span>
      </div>
      <ul
        aria-label="Sampled video frames"
        className="cm-evidence-reel"
        onKeyDown={(event) => {
          if (event.key === "ArrowRight") {
            event.preventDefault();
            setSelected((value) =>
              Math.min(value + 1, artifact.frames.length - 1),
            );
          }
          if (event.key === "ArrowLeft") {
            event.preventDefault();
            setSelected((value) => Math.max(value - 1, 0));
          }
          if (event.key === "Enter") {
            event.preventDefault();
            setDetailsOpen(true);
          }
          if (event.key === "Escape") {
            setDetailsOpen(false);
          }
        }}
      >
        {artifact.frames.map((frame, index) => (
          <li key={frame.id}>
            <button
              aria-label={`${frame.id} at ${frame.timestampSec.toFixed(1)} seconds`}
              aria-pressed={selected === index}
              className="cm-frame-button"
              onClick={() => {
                setSelected(index);
                setDetailsOpen(true);
              }}
              type="button"
            >
              <Image
                alt=""
                className="cm-frame-image"
                height={88}
                loading={index > 3 ? "lazy" : "eager"}
                src={frame.thumbnailUrl}
                style={{ height: "88px", width: "100%" }}
                unoptimized
                width={180}
              />
              <span className="cm-frame-label">
                <span>{frame.id}</span>
                <span>
                  {frame.kind === "motion_strip"
                    ? "motion"
                    : `${frame.timestampSec.toFixed(1)}s`}
                </span>
              </span>
            </button>
          </li>
        ))}
      </ul>
      <div className="mt-5 grid gap-3 rounded-lg border border-[var(--cm-line)] p-4">
        <div className="flex flex-wrap items-center gap-2">
          <span className="cm-chip cm-chip-gold">
            <ScanSearch size={14} />
            Selected {selectedFrame.id}
          </span>
          <span className="cm-chip">
            {selectedFrame.timestampSec.toFixed(1)} seconds
          </span>
          <span className="cm-chip">
            {selectedFrame.kind.replace("_", " ")}
          </span>
        </div>
        {detailsOpen ? (
          <div className="grid gap-2">
            <p className="cm-muted text-sm">Supported evidence links</p>
            <div className="flex flex-wrap gap-2">
              {supportedSegments.map((segment) => (
                <span className="cm-chip cm-chip-gold" key={segment.id}>
                  {segment.id}: {segment.summary}
                </span>
              ))}
            </div>
          </div>
        ) : (
          <p className="cm-muted text-sm">
            Press Enter or click a frame to open frame details.
          </p>
        )}
      </div>
    </section>
  );
}
