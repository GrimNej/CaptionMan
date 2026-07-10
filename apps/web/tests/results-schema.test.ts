import { describe, expect, it } from "vitest";
import { resultsEnvelopeSchema } from "../lib/schemas";

describe("results schema", () => {
  it("accepts CaptionMan output", () => {
    const parsed = resultsEnvelopeSchema.parse([
      {
        task_id: "demo",
        captions: {
          formal: "Formal",
          sarcastic: "Sarcastic",
          humorous_tech: "Tech",
          humorous_non_tech: "Non tech",
        },
      },
    ]);
    expect(parsed).toHaveLength(1);
  });
});
