import { Clapperboard, ShieldCheck } from "lucide-react";
import { ProviderStatusMini } from "@/components/evidence-cinema/provider-status-mini";
import { RunHistoryPanel } from "@/components/evidence-cinema/run-history-panel";
import { RunLauncherPanel } from "@/components/evidence-cinema/run-launcher-panel";
import { SubmissionReadinessStrip } from "@/components/evidence-cinema/submission-readiness-strip";
import { Shell } from "@/components/layout/shell";

export default function RunStudioPage() {
  return (
    <Shell>
      <main className="cm-page grid gap-6">
        <section className="cm-studio-hero cm-panel p-6 md:p-8">
          <div className="grid gap-5 lg:grid-cols-[1fr_0.9fr]">
            <div>
              <span className="cm-kicker">
                <Clapperboard size={15} />
                Run Studio
              </span>
              <h1 className="cm-section-title mt-4">
                Add videos. Caption them. Review the proof.
              </h1>
              <a className="cm-button cm-button-primary mt-5" href="#workbench">
                <Clapperboard size={16} />
                Start captioning
              </a>
            </div>
            <div className="grid content-start gap-4">
              <ProviderStatusMini />
              <div className="cm-panel-soft p-4">
                <span className="cm-kicker">
                  <ShieldCheck size={15} />
                  Current rule
                </span>
                <p className="mt-3 text-lg font-semibold">
                  Paste a video URL or upload a file, then inspect captions,
                  evidence, and verdict.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section id="workbench">
          <RunLauncherPanel />
        </section>

        <section className="grid gap-5 lg:grid-cols-[1fr_0.82fr]">
          <RunHistoryPanel />
          <div className="cm-panel p-6">
            <span className="cm-kicker">Docker readiness</span>
            <p className="mt-3 text-xl font-semibold">
              Docker remains the judged path.
            </p>
            <p className="cm-muted mt-2 text-sm leading-6">
              Studio is for inspection. The submitted image still reads
              `/input/tasks.json` and writes `/output/results.json`.
            </p>
          </div>
        </section>
        <SubmissionReadinessStrip />
      </main>
    </Shell>
  );
}
