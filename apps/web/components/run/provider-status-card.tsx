import { ShieldCheck } from "lucide-react";

export function ProviderStatusCard() {
  return (
    <div className="court">
      <div className="court-row">
        <span>
          <ShieldCheck size={16} /> Caption Provider
        </span>
        <span className="score">ready</span>
      </div>
      <p className="muted">
        Fireworks readiness is verified by the backend doctor command.
      </p>
    </div>
  );
}
