import { describe, expect, it } from "vitest";
import { artifactFromApiArtifacts } from "../lib/replay-artifact";

describe("replay artifact adapter", () => {
  it("adapts backend replay and official results for Evidence Cinema", () => {
    const artifact = artifactFromApiArtifacts({
      runId: "run-001",
      replay: [
        {
          video_id: "v1",
          evidence: {
            overall_summary: "Traffic moves along an autumn boulevard.",
            frame_artifacts: [
              {
                frame_id: "F01",
                timestamp_seconds: 1.5,
                image_path: "fireworks/v1/frames/frame-000.jpg",
                kind: "single_frame",
              },
            ],
            segments: [
              {
                start_seconds: 0,
                end_seconds: 10,
                observations: ["Golden trees line a street with moving cars."],
              },
            ],
            forbidden_assumptions: ["Do not infer exact location."],
          },
          caption_court: [
            {
              style: "formal",
              candidates: ["Traffic moves along an autumn boulevard."],
              selected: "Traffic moves along an autumn boulevard.",
            },
          ],
          budget: { model_calls_used: 5, max_model_calls: 5 },
        },
      ],
      results: [
        {
          task_id: "v1",
          captions: {
            formal: "Traffic moves along an autumn boulevard.",
            sarcastic: "Golden trees try to make traffic look poetic.",
            humorous_tech:
              "Traffic streams through the scene like motion data.",
            humorous_non_tech:
              "Autumn makes the traffic look better than usual.",
          },
        },
      ],
    });

    expect(artifact.runId).toBe("run-001");
    expect(artifact.video.id).toBe("v1");
    expect(artifact.finalCaptions.formal).toContain("Traffic");
    expect(artifact.frames[0]?.thumbnailUrl).toContain(
      "/api/runs/run-001/artifacts/frames/F01",
    );
    expect(artifact.evidenceSegments[0]?.supportedBy.length).toBeGreaterThan(0);
  });

  it("accepts single-object replay and result artifacts", () => {
    const artifact = artifactFromApiArtifacts({
      runId: "run-single",
      replay: {
        video_id: "v1",
        evidence: {
          overall_summary: "Traffic moves along an autumn boulevard.",
          frame_artifacts: [
            {
              frame_id: "F01",
              timestamp_seconds: 1.5,
              image_path: "fireworks/v1/frames/frame-000.jpg",
            },
          ],
        },
      },
      results: {
        task_id: "v1",
        captions: {
          formal: "Traffic moves along an autumn boulevard.",
          sarcastic: "Golden trees try to make traffic look poetic.",
          humorous_tech: "Traffic streams through the scene like motion data.",
          humorous_non_tech: "Autumn makes the traffic look better than usual.",
        },
      },
    });

    expect(artifact.frames[0]?.thumbnailUrl).toContain(
      "/api/runs/run-single/artifacts/frames/F01",
    );
  });
});
