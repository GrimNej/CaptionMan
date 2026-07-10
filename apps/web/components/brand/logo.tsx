import { Clapperboard } from "lucide-react";

export function Logo() {
  return (
    <span className="brand">
      <span className="brand-mark">
        <Clapperboard size={21} />
      </span>
      <span>CaptionMan</span>
    </span>
  );
}
