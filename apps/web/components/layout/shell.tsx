import { Clapperboard, ExternalLink, FileCheck2, Gauge } from "lucide-react";
import Link from "next/link";

export function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div className="cm-shell">
      <header className="cm-topbar">
        <Link className="cm-brand" href="/">
          <span className="cm-brand-mark">
            <Clapperboard size={21} />
          </span>
          <span>
            <h1 className="cm-brand-title">CaptionMan</h1>
            <p className="cm-brand-tagline">Captions With Receipts</p>
          </span>
        </Link>
        <nav className="cm-nav" aria-label="Primary">
          <Link className="cm-nav-link" href="/studio">
            <Gauge size={15} />
            Run Studio
          </Link>
          <Link className="cm-nav-link" href="/submission">
            <FileCheck2 size={15} />
            Docker Readiness
          </Link>
          <a
            className="cm-nav-link"
            href="https://grimnej.com"
            rel="noreferrer"
            target="_blank"
          >
            <ExternalLink size={15} />
            My Portfolio
          </a>
        </nav>
      </header>
      {children}
    </div>
  );
}
