import { CheckCircle2 } from "lucide-react";

const items = [
  "Docker runner",
  "Provider route",
  "Schema adapter",
  "Output validator",
  "No secrets",
  "Frontend build",
  "Reduced motion",
];

export function SubmissionReadinessStrip() {
  return (
    <section aria-label="Submission readiness" className="cm-readiness">
      {items.map((item) => (
        <div className="cm-panel-soft flex items-center gap-2 p-3" key={item}>
          <CheckCircle2 color="var(--cm-verified-teal)" size={16} />
          <span className="text-sm">{item}</span>
        </div>
      ))}
    </section>
  );
}
