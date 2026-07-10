"use client";

import { motion, useReducedMotion } from "motion/react";

function highlightTerms(text: string, terms: string[], className: string) {
  if (terms.length === 0) {
    return text;
  }
  const pattern = new RegExp(
    `(${terms.map((term) => term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})`,
    "gi",
  );
  return text.split(pattern).map((part) => {
    const matched = terms.some(
      (term) => term.toLowerCase() === part.toLowerCase(),
    );
    return matched ? (
      <mark className={className} key={`${part}-${text.length}`}>
        {part}
      </mark>
    ) : (
      part
    );
  });
}

export function RepairDiff({
  before,
  after,
  reasons,
  unsupportedTerms,
}: {
  before: string;
  after: string;
  reasons: string[];
  unsupportedTerms: string[];
}) {
  const reduceMotion = useReducedMotion();
  const saferTerms = after
    .split(/\s+/)
    .map((term) => term.replace(/^[^\w]+|[^\w]+$/g, ""))
    .filter((term) => term.length > 5)
    .slice(0, 4);

  return (
    <motion.section
      className="cm-panel p-5"
      initial={false}
      animate={reduceMotion ? undefined : { y: 0 }}
      transition={{ duration: 0.24, ease: "easeOut" }}
    >
      <div className="mb-5">
        <span className="cm-kicker">Repair Diff</span>
        <h2 className="mt-2 text-2xl font-semibold">
          Unsupported claims corrected
        </h2>
      </div>
      <div className="cm-diff">
        <div className="cm-diff-panel">
          <p className="cm-muted mb-2 text-xs uppercase tracking-wide">
            Before
          </p>
          <p className="text-lg leading-relaxed">
            {highlightTerms(before, unsupportedTerms, "cm-mark-ruby")}
          </p>
        </div>
        <div className="cm-diff-panel">
          <p className="cm-muted mb-2 text-xs uppercase tracking-wide">After</p>
          <p className="text-lg leading-relaxed">
            {highlightTerms(after, saferTerms, "cm-mark-gold")}
          </p>
        </div>
      </div>
      <ul className="mt-5 grid gap-2">
        {reasons.map((reason) => (
          <li className="cm-chip cm-chip-ruby justify-start" key={reason}>
            {reason}
          </li>
        ))}
      </ul>
    </motion.section>
  );
}
