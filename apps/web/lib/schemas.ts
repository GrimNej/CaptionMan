import { z } from "zod";

export const CaptionStyleSchema = z.enum([
  "formal",
  "sarcastic",
  "humorous_tech",
  "humorous_non_tech",
]);

export const JudgeReplayArtifactSchema = z.object({
  runId: z.string(),
  video: z.object({
    id: z.string(),
    title: z.string().optional(),
    durationSec: z.number(),
    previewUrl: z.string().optional(),
  }),
  frames: z.array(
    z.object({
      id: z.string(),
      timestampSec: z.number(),
      thumbnailUrl: z.string(),
      kind: z.enum(["single_frame", "motion_strip"]),
    }),
  ),
  evidenceSegments: z.array(
    z.object({
      id: z.string(),
      startSec: z.number(),
      endSec: z.number(),
      summary: z.string(),
      supportedBy: z.array(z.string()),
      avoidClaims: z.array(z.string()),
      confidence: z.number(),
    }),
  ),
  court: z.array(
    z.object({
      style: CaptionStyleSchema,
      candidates: z.array(
        z.object({
          id: z.string(),
          caption: z.string(),
          factuality: z.number(),
          tone: z.number(),
          omission: z.number(),
          risk: z.enum(["low", "medium", "high"]),
          selected: z.boolean(),
          unsupportedTerms: z.array(z.string()).default([]),
        }),
      ),
      repair: z
        .object({
          before: z.string(),
          after: z.string(),
          reasons: z.array(z.string()),
        })
        .optional(),
    }),
  ),
  finalCaptions: z.object({
    formal: z.string(),
    sarcastic: z.string(),
    humorous_tech: z.string(),
    humorous_non_tech: z.string(),
  }),
});

export type CaptionStyle = z.infer<typeof CaptionStyleSchema>;
export type JudgeReplayArtifact = z.infer<typeof JudgeReplayArtifactSchema>;

export const resultSchema = z.object({
  task_id: z.string(),
  captions: z.object({
    formal: z.string(),
    sarcastic: z.string(),
    humorous_tech: z.string(),
    humorous_non_tech: z.string(),
  }),
});

export const resultsEnvelopeSchema = z.array(resultSchema);
