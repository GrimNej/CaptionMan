import { CheckCircle2, ClipboardCheck, Terminal } from "lucide-react";
import Link from "next/link";
import { SubmissionReadinessStrip } from "@/components/evidence-cinema/submission-readiness-strip";
import { Shell } from "@/components/layout/shell";

const checks = [
  "Docker image builds",
  "Docker doctor passes",
  "Runner writes /output/results.json",
  "Official Track 2 schema validates",
  "Source hygiene passes",
  "No secrets detected",
  "Frontend build passes",
];

export default function SubmissionConsolePage() {
  return (
    <Shell>
      <main className="cm-page grid gap-6">
        <section className="cm-panel p-8 md:p-10">
          <span className="cm-kicker">
            <ClipboardCheck size={15} />
            Docker Readiness
          </span>
          <h1 className="cm-section-title mt-4">
            Ready for the judged Docker runner.
          </h1>
          <p className="cm-body mt-4 max-w-3xl">
            Compact readiness view for the Dockerized Track 2 path. The frontend
            stays separate from judged output.
          </p>
        </section>
        <SubmissionReadinessStrip />
        <section className="grid gap-5 lg:grid-cols-[0.8fr_1.2fr]">
          <div className="cm-panel p-5">
            <h2 className="mb-4 text-2xl font-semibold">Checklist</h2>
            <div className="grid gap-3">
              {checks.map((check) => (
                <div
                  className="cm-panel-soft flex items-center gap-3 p-3"
                  key={check}
                >
                  <CheckCircle2 color="var(--cm-verified-teal)" size={18} />
                  <span>{check}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="cm-panel p-5">
            <div className="mb-4 flex items-center gap-2">
              <Terminal color="var(--cm-evidence-gold)" size={18} />
              <h2 className="text-2xl font-semibold">Docker gate</h2>
            </div>
            <pre className="cm-json">{`docker build -t captionman .
docker run --rm captionman captionman doctor
docker run --rm -v "$PWD/input:/input" -v "$PWD/output:/output" captionman
python scripts/validate_results.py output/results.json`}</pre>
            <Link className="cm-button cm-button-primary mt-5" href="/studio">
              Run a video
            </Link>
          </div>
        </section>
      </main>
    </Shell>
  );
}
