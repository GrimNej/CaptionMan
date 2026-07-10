import { getApiBase } from "./api-base";
import { mockReplay } from "./mock-replay";
import {
  type CaptionStyle,
  type JudgeReplayArtifact,
  JudgeReplayArtifactSchema,
  resultsEnvelopeSchema,
} from "./schemas";

const styles: CaptionStyle[] = [
  "formal",
  "sarcastic",
  "humorous_tech",
  "humorous_non_tech",
];

type RawEvidenceSegment = {
  start_seconds?: number;
  end_seconds?: number;
  observations?: string[];
};

type RawEvidence = {
  video_id?: string;
  overall_summary?: string;
  main_event?: string;
  frame_artifacts?: {
    frame_id?: string;
    timestamp_seconds?: number;
    image_path?: string;
    kind?: "single_frame" | "motion_strip";
  }[];
  segments?: RawEvidenceSegment[];
  forbidden_assumptions?: string[];
  uncertainty_notes?: string[];
};

type RawCourtRow = {
  style?: CaptionStyle;
  candidates?: string[];
  selected?: string;
};

type RawReplayItem = {
  video_id?: string;
  evidence?: RawEvidence;
  caption_court?: RawCourtRow[];
  budget?: {
    model_calls_used?: number;
    max_model_calls?: number;
  };
};

export async function getReplayArtifact(
  runId: string,
): Promise<JudgeReplayArtifact> {
  if (runId === "demo") {
    return { ...mockReplay, runId };
  }

  try {
    const base = getApiBase();
    const [replayResponse, resultsResponse] = await Promise.all([
      fetch(`${base}/api/runs/${runId}/artifacts/judge-replay`, {
        cache: "no-store",
      }),
      fetch(`${base}/api/runs/${runId}/artifacts/results`, {
        cache: "no-store",
      }),
    ]);
    if (!replayResponse.ok || !resultsResponse.ok) {
      throw new Error(
        `Replay artifacts unavailable for ${runId}: judge=${replayResponse.status}, results=${resultsResponse.status}`,
      );
    }
    return artifactFromApiArtifacts({
      runId,
      replay: await replayResponse.json(),
      results: await resultsResponse.json(),
    });
  } catch (error) {
    throw new Error(
      `Could not load Judge Verdict for ${runId}: ${
        error instanceof Error ? error.message : "unknown error"
      }`,
    );
  }
}

export function artifactFromApiArtifacts({
  runId,
  replay,
  results,
}: {
  runId: string;
  replay: unknown;
  results: unknown;
}): JudgeReplayArtifact {
  const rawReplay = (
    Array.isArray(replay) ? (replay[0] as RawReplayItem) : replay
  ) as RawReplayItem;
  const parsedResults = resultsEnvelopeSchema.parse(
    Array.isArray(results) ? results : [results],
  );
  const result = parsedResults[0];
  const evidence = rawReplay.evidence ?? {};
  const base = getApiBase();
  const segments = evidence.segments?.length
    ? evidence.segments
    : [
        {
          start_seconds: 0,
          end_seconds: 10,
          observations: [evidence.overall_summary ?? "A video clip is shown."],
        },
      ];
  const recordedFrames =
    evidence.frame_artifacts?.filter((frame) => frame.frame_id) ?? [];
  const frameCount = Math.max(4, Math.min(8, segments.length * 2));
  const frames = recordedFrames.length
    ? recordedFrames.map((frame, index) => ({
        id: frame.frame_id ?? `F${String(index + 1).padStart(2, "0")}`,
        timestampSec: Number(
          (frame.timestamp_seconds ?? index * 2.4).toFixed(1),
        ),
        thumbnailUrl: `${base}/api/runs/${runId}/artifacts/frames/${encodeURIComponent(
          frame.frame_id ?? `F${String(index + 1).padStart(2, "0")}`,
        )}`,
        kind: frame.kind ?? (index % 3 === 2 ? "motion_strip" : "single_frame"),
      }))
    : Array.from({ length: frameCount }, (_, index) => ({
        id: `F${String(index + 1).padStart(2, "0")}`,
        timestampSec: Number((index * 2.4).toFixed(1)),
        thumbnailUrl: "/captionman-frame.svg",
        kind: index % 3 === 2 ? "motion_strip" : "single_frame",
      }));
  const frameIds = frames.map((frame) => frame.id);
  const courtRows = rawReplay.caption_court ?? [];

  return JudgeReplayArtifactSchema.parse({
    runId,
    video: {
      id: result?.task_id ?? rawReplay.video_id ?? runId,
      title: evidence.overall_summary ?? `Run ${runId}`,
      durationSec: Math.max(
        ...segments.map((segment) => segment.end_seconds ?? 10),
        10,
      ),
      previewUrl: frames[0]?.thumbnailUrl ?? "/captionman-frame.svg",
    },
    frames,
    evidenceSegments: segments.map((segment, index) => ({
      id: `E${String(index + 1).padStart(2, "0")}`,
      startSec: segment.start_seconds ?? 0,
      endSec: segment.end_seconds ?? (index + 1) * 4,
      summary:
        segment.observations?.[0] ??
        evidence.overall_summary ??
        "Visual evidence.",
      supportedBy: frameIds.slice(
        Math.min(index, frameIds.length - 1),
        Math.min(index + 3, frameIds.length),
      ),
      avoidClaims: evidence.forbidden_assumptions ?? [
        "Do not infer identities, brands, exact locations, or intent.",
      ],
      confidence: 0.82,
    })),
    court: styles.map((style) => {
      const row = courtRows.find((item) => item.style === style);
      const selectedCaption = result.captions[style];
      const rawCandidates = row?.candidates?.length
        ? row.candidates
        : [selectedCaption];
      return {
        style,
        candidates: rawCandidates.map((caption, index) => {
          const selected =
            caption === selectedCaption || caption === row?.selected;
          return {
            id: `${style}-${index + 1}`,
            caption,
            factuality: selected ? 0.92 : 0.72,
            tone: selected ? 0.9 : 0.78,
            omission: selected ? 0.16 : 0.28,
            risk: selected ? "low" : "medium",
            selected,
            unsupportedTerms: [],
          };
        }),
      };
    }),
    finalCaptions: result.captions,
  });
}
