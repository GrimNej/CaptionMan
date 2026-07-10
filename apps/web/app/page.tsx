import {
  ArrowRight,
  Film,
  ScrollText,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import Link from "next/link";
import { ProviderStatusMini } from "@/components/evidence-cinema/provider-status-mini";
import { SubmissionReadinessStrip } from "@/components/evidence-cinema/submission-readiness-strip";
import { Shell } from "@/components/layout/shell";

export default function ScreeningRoomPage() {
  return (
    <Shell>
      <main className="cm-page grid gap-8">
        <section className="cm-landing-hero">
          <div className="cm-landing-hero-content">
            <span className="cm-kicker">
              <Film size={15} />
              Track 2 Video Captioning
            </span>
            <h1 className="cm-hero-title mt-6">CaptionMan</h1>
            <p className="mt-5 text-2xl font-semibold text-[var(--cm-evidence-gold)]">
              Captions With Receipts
            </p>
            <p className="cm-body mt-6 max-w-2xl">
              A judge-aware captioning system that watches each clip, builds
              evidence, challenges weak captions, and exports the official
              four-style Track 2 result.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link className="cm-button cm-button-primary" href="/studio">
                Test the real runner
                <ArrowRight size={16} />
              </Link>
              <Link className="cm-button" href="/submission">
                Review Docker path
              </Link>
            </div>
          </div>
          <div className="cm-landing-hero-badges">
            <span className="cm-chip cm-chip-gold">
              <ShieldCheck size={14} />
              schema-ready
            </span>
            <span className="cm-chip cm-chip-teal">
              <Sparkles size={14} />
              accuracy + tone
            </span>
          </div>
        </section>
        <section className="cm-panel p-5">
          <div className="mb-5 flex flex-wrap items-center justify-between gap-4">
            <div>
              <span className="cm-kicker">
                <ScrollText size={15} />
                Preview
              </span>
              <h2 className="mt-2 text-2xl font-semibold">
                Evidence, court, verdict, export
              </h2>
            </div>
            <ProviderStatusMini />
          </div>
          <SubmissionReadinessStrip />
        </section>
      </main>
    </Shell>
  );
}
