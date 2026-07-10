"use client";

import { AlertTriangle, CheckCircle2, RadioTower, WifiOff } from "lucide-react";
import { useEffect, useState } from "react";
import { getApiBase } from "@/lib/api-base";

type DoctorState =
  | { status: "loading" }
  | {
      status: "online";
      ok: boolean;
      provider: string;
      route: string;
      captionModel: string;
      gemmaActive: boolean;
    }
  | { status: "offline"; message: string };

export function ProviderStatusMini({ compact = false }: { compact?: boolean }) {
  const [state, setState] = useState<DoctorState>({ status: "loading" });

  useEffect(() => {
    let ignore = false;
    async function load() {
      try {
        const base = getApiBase();
        const response = await fetch(`${base}/api/doctor?live=false`, {
          cache: "no-store",
        });
        if (!response.ok) {
          throw new Error(`API returned ${response.status}`);
        }
        const payload = await response.json();
        if (ignore) {
          return;
        }
        setState({
          status: "online",
          ok: Boolean(payload.ok),
          provider: String(payload.checks?.mode?.ai_provider ?? "unknown"),
          route: String(payload.checks?.routing?.champion_route ?? "unknown"),
          captionModel: String(
            payload.checks?.routing?.caption_model ?? "not selected",
          ),
          gemmaActive: Boolean(payload.checks?.routing?.gemma?.active),
        });
      } catch (error) {
        if (ignore) {
          return;
        }
        setState({
          status: "offline",
          message: error instanceof Error ? error.message : "API unavailable",
        });
      }
    }
    load();
    return () => {
      ignore = true;
    };
  }, []);

  if (state.status === "loading") {
    return (
      <div className="cm-provider-mini cm-panel-soft flex flex-wrap items-center gap-2 p-3">
        <RadioTower color="var(--cm-evidence-gold)" size={16} />
        <span className="cm-chip">Checking API</span>
      </div>
    );
  }

  if (state.status === "offline") {
    return (
      <div className="cm-provider-mini cm-provider-mini-danger cm-panel-soft flex flex-wrap items-center gap-2 p-3">
        <WifiOff color="var(--cm-risk-ruby)" size={16} />
        <span className="cm-chip cm-chip-ruby">API offline</span>
        <span className="cm-chip">{state.message}</span>
      </div>
    );
  }

  return (
    <div className="cm-provider-mini cm-panel-soft flex flex-wrap items-center gap-2 p-3">
      {state.ok ? (
        <CheckCircle2 color="var(--cm-verified-teal)" size={16} />
      ) : (
        <AlertTriangle color="var(--cm-status-warning)" size={16} />
      )}
      <span className={state.ok ? "cm-chip cm-chip-teal" : "cm-chip"}>
        API {state.ok ? "ready" : "needs attention"}
      </span>
      <span className="cm-chip">Caption engine</span>
      {state.provider !== "mock" ? (
        <span className="cm-chip">Route: {state.route}</span>
      ) : null}
      {!compact && state.provider !== "mock" ? (
        <span className="cm-chip">Caption: {state.captionModel}</span>
      ) : null}
      {state.gemmaActive ? (
        <span className="cm-chip cm-chip-teal">Gemma active</span>
      ) : null}
    </div>
  );
}
