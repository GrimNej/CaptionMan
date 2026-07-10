"use client";

import { motion, useReducedMotion } from "motion/react";

export function VerdictStamp({
  label = "Selected verdict",
}: {
  label?: string;
}) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.div
      aria-label={label}
      className="absolute right-4 top-4 z-10"
      initial={false}
      animate={reduceMotion ? undefined : { rotate: -5, scale: 1 }}
      transition={{ duration: 0.55, ease: "easeOut" }}
    >
      <svg
        aria-hidden="true"
        className="h-24 w-24"
        role="img"
        viewBox="0 0 120 120"
      >
        <title>{label}</title>
        <circle
          cx="60"
          cy="60"
          fill="none"
          r="45"
          stroke="var(--cm-evidence-gold)"
          strokeDasharray="7 5"
          strokeWidth="3"
        />
        <circle
          cx="60"
          cy="60"
          fill="rgba(214, 177, 94, 0.08)"
          r="36"
          stroke="var(--cm-evidence-gold)"
          strokeWidth="2"
        />
        <text
          fill="var(--cm-evidence-gold)"
          fontSize="12"
          fontWeight="800"
          letterSpacing="1.5"
          textAnchor="middle"
          x="60"
          y="55"
        >
          FINAL
        </text>
        <text
          fill="var(--cm-evidence-gold)"
          fontSize="13"
          fontWeight="900"
          letterSpacing="1.2"
          textAnchor="middle"
          x="60"
          y="72"
        >
          VERDICT
        </text>
      </svg>
    </motion.div>
  );
}
