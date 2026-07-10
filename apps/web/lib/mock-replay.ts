import { type JudgeReplayArtifact, JudgeReplayArtifactSchema } from "./schemas";

const thumbnail = "/captionman-frame.svg";

export const mockReplay: JudgeReplayArtifact = JudgeReplayArtifactSchema.parse({
  runId: "demo",
  video: {
    id: "v2",
    title: "Practice clip: kitchen evidence repair",
    durationSec: 18.25,
    previewUrl: thumbnail,
  },
  frames: [
    {
      id: "F01",
      timestampSec: 0.4,
      thumbnailUrl: thumbnail,
      kind: "single_frame",
    },
    {
      id: "F02",
      timestampSec: 2.1,
      thumbnailUrl: thumbnail,
      kind: "single_frame",
    },
    {
      id: "F03",
      timestampSec: 4.8,
      thumbnailUrl: thumbnail,
      kind: "motion_strip",
    },
    {
      id: "F04",
      timestampSec: 6.2,
      thumbnailUrl: thumbnail,
      kind: "single_frame",
    },
    {
      id: "F05",
      timestampSec: 8.7,
      thumbnailUrl: thumbnail,
      kind: "single_frame",
    },
    {
      id: "F06",
      timestampSec: 11.2,
      thumbnailUrl: thumbnail,
      kind: "motion_strip",
    },
    {
      id: "F07",
      timestampSec: 14.3,
      thumbnailUrl: thumbnail,
      kind: "single_frame",
    },
    {
      id: "F08",
      timestampSec: 17.6,
      thumbnailUrl: thumbnail,
      kind: "single_frame",
    },
  ],
  evidenceSegments: [
    {
      id: "E01",
      startSec: 0,
      endSec: 5.5,
      summary:
        "A person is visible indoors near a counter with food preparation activity.",
      supportedBy: ["F01", "F02", "F03"],
      avoidClaims: ["chef", "restaurant", "professional kitchen"],
      confidence: 0.82,
    },
    {
      id: "E02",
      startSec: 5.5,
      endSec: 12.5,
      summary:
        "Hands and kitchen-like surfaces appear as the action continues at close range.",
      supportedBy: ["F03", "F04", "F05", "F06"],
      avoidClaims: ["specific recipe", "brand names", "exact location"],
      confidence: 0.78,
    },
    {
      id: "E03",
      startSec: 12.5,
      endSec: 18.25,
      summary:
        "The clip remains focused on indoor preparation rather than a wider room context.",
      supportedBy: ["F06", "F07", "F08"],
      avoidClaims: ["restaurant service", "named identity", "completed dish"],
      confidence: 0.74,
    },
  ],
  court: [
    {
      style: "formal",
      candidates: [
        {
          id: "formal-a",
          caption: "A chef prepares food in a restaurant kitchen.",
          factuality: 0.54,
          tone: 0.93,
          omission: 0.28,
          risk: "high",
          selected: false,
          unsupportedTerms: ["chef", "restaurant"],
        },
        {
          id: "formal-b",
          caption: "A person prepares food in an indoor kitchen-like setting.",
          factuality: 0.93,
          tone: 0.9,
          omission: 0.18,
          risk: "low",
          selected: true,
          unsupportedTerms: [],
        },
      ],
      repair: {
        before: "A chef prepares food in a restaurant kitchen.",
        after: "A person prepares food in an indoor kitchen-like setting.",
        reasons: [
          "The evidence supports food preparation indoors, but not the person's profession.",
          "The frames do not prove a restaurant setting.",
        ],
      },
    },
    {
      style: "sarcastic",
      candidates: [
        {
          id: "sarcastic-a",
          caption:
            "A person prepares food indoors, because apparently dinner needed witnesses.",
          factuality: 0.88,
          tone: 0.9,
          omission: 0.22,
          risk: "low",
          selected: true,
        },
        {
          id: "sarcastic-b",
          caption: "A famous chef dominates a luxury restaurant kitchen.",
          factuality: 0.38,
          tone: 0.8,
          omission: 0.32,
          risk: "high",
          selected: false,
          unsupportedTerms: ["famous", "chef", "luxury restaurant"],
        },
      ],
    },
    {
      style: "humorous_tech",
      candidates: [
        {
          id: "tech-a",
          caption:
            "Food prep runs in foreground mode while the evidence thread keeps logging frames.",
          factuality: 0.84,
          tone: 0.89,
          omission: 0.24,
          risk: "low",
          selected: true,
        },
        {
          id: "tech-b",
          caption:
            "The chef deploys dinner from a restaurant production server.",
          factuality: 0.48,
          tone: 0.86,
          omission: 0.31,
          risk: "high",
          selected: false,
          unsupportedTerms: ["chef", "restaurant"],
        },
      ],
    },
    {
      style: "humorous_non_tech",
      candidates: [
        {
          id: "nontech-a",
          caption:
            "Someone is making food indoors, and the countertop is getting its close-up.",
          factuality: 0.9,
          tone: 0.86,
          omission: 0.2,
          risk: "low",
          selected: true,
        },
        {
          id: "nontech-b",
          caption:
            "A restaurant chef whips up a masterpiece for a packed dinner rush.",
          factuality: 0.4,
          tone: 0.82,
          omission: 0.35,
          risk: "high",
          selected: false,
          unsupportedTerms: [
            "restaurant chef",
            "masterpiece",
            "packed dinner rush",
          ],
        },
      ],
    },
  ],
  finalCaptions: {
    formal: "A person prepares food in an indoor kitchen-like setting.",
    sarcastic:
      "A person prepares food indoors, because apparently dinner needed witnesses.",
    humorous_tech:
      "Food prep runs in foreground mode while the evidence thread keeps logging frames.",
    humorous_non_tech:
      "Someone is making food indoors, and the countertop is getting its close-up.",
  },
});
