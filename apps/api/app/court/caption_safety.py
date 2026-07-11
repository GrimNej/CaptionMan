from __future__ import annotations

import json
import re

from app.evidence.evidence_schema import EvidenceGraph
from app.providers.base import CaptionStyle

MAX_FINAL_CAPTION_CHARS = 320
MAX_FINAL_CAPTION_WORDS = 26

META_FRAGMENTS = (
    "the user",
    "word count",
    "count characters",
    "return json",
    "json object",
    "system prompt",
    "reasoning:",
    "analysis:",
    "contact sheet",
    "sampled frame",
    "frames labeled",
    "caption:",
)

SPECULATIVE_INTENT_PATTERNS = (
    r"\b(?:apparently|probably|presumably|supposedly)\b",
    r"\b(?:expect(?:s|ed|ing)?|hop(?:e|es|ed|ing)|plan(?:s|ned|ning)?|pretend(?:s|ed|ing)?|wait(?:s|ed|ing)?|want(?:s|ed|ing)?|wish(?:es|ed|ing)?)\b",
    r"\b(?:thinking|deciding) to\b",
)

CANNED_STYLE_PATTERNS = (
    r"\bah yes\b",
    r"\banother heroic day\b",
    r"\bbehold\b",
    r"\bbecause nothing\b",
    r"\bnothing says\b",
    r"\bproving once again\b",
)

PRODUCTION_ARTIFACT_PATTERNS = (
    r"\bcompress\w*\b.{0,40}\b"
    r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve) seconds?\b",
)

ASCII_PUNCTUATION = str.maketrans(
    {
        "\u00a0": " ",
        "\u2011": "-",
        "\u2013": "-",
        "\u2014": " - ",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
    }
)

DANGLING_WORDS = {
    "a",
    "against",
    "an",
    "and",
    "around",
    "as",
    "at",
    "because",
    "beneath",
    "between",
    "but",
    "by",
    "for",
    "from",
    "in",
    "inside",
    "into",
    "near",
    "of",
    "on",
    "or",
    "outside",
    "over",
    "the",
    "through",
    "to",
    "toward",
    "towards",
    "under",
    "while",
    "with",
}


def ensure_safe_caption(caption: str, evidence: EvidenceGraph, style: CaptionStyle) -> str:
    cleaned = clean_caption(caption)
    if not caption_is_usable(cleaned):
        return fallback_caption(evidence, style)
    return cleaned


def caption_is_usable(caption: str) -> bool:
    if not caption or len(caption) < 12 or len(caption.split()) < 3:
        return False
    if len(caption.split()) > MAX_FINAL_CAPTION_WORDS:
        return False
    lowered = caption.lower()
    if any(fragment in lowered for fragment in META_FRAGMENTS):
        return False
    if any(re.search(pattern, lowered) for pattern in SPECULATIVE_INTENT_PATTERNS):
        return False
    if any(re.search(pattern, lowered) for pattern in CANNED_STYLE_PATTERNS):
        return False
    if any(re.search(pattern, lowered) for pattern in PRODUCTION_ARTIFACT_PATTERNS):
        return False
    if re.search(r"\b(?:f|frame)\s*0?\d+\b", lowered):
        return False
    if re.search(r"\b(?:four|4)\s+(?:frames|samples|stages|takes|poses)\b", lowered):
        return False
    if re.search(r"\b(that'?s|that is)\s+\d+\s+words\b", lowered):
        return False
    if caption.startswith(("{", "[")) or "```" in caption or "\n" in caption:
        return False
    if caption.count('"') % 2 == 1:
        return False
    terminal_word = re.sub(r"[^a-z]+$", "", lowered).rsplit(" ", 1)[-1]
    if terminal_word in DANGLING_WORDS:
        return False
    return bool(re.search(r"[a-z]", lowered))


def clean_caption(caption: str, limit: int = MAX_FINAL_CAPTION_CHARS) -> str:
    cleaned = caption.translate(ASCII_PUNCTUATION).strip()
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE)
    extracted = _caption_from_json(cleaned)
    if extracted is not None:
        cleaned = extracted
    lines = [line.strip(" -\t") for line in cleaned.splitlines() if line.strip()]
    if len(lines) > 1:
        non_meta = [
            re.sub(r"(?i)^caption\s*:\s*", "", line)
            for line in lines
            if not re.match(r"(?i)^(analysis|reasoning|answer)\s*:", line)
        ]
        cleaned = " ".join(non_meta or lines)
    cleaned = re.sub(r"(?i)^caption\s*:\s*", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip().strip('"')
    if not cleaned:
        return ""
    if len(cleaned) > limit:
        clipped = cleaned[:limit]
        sentence_end = max(clipped.rfind("."), clipped.rfind("!"), clipped.rfind("?"))
        if sentence_end >= 24:
            cleaned = clipped[: sentence_end + 1]
        else:
            cleaned = clipped.rsplit(" ", 1)[0].rstrip(" ,;:-")
    if cleaned and cleaned[-1] not in ".!?":
        cleaned += "."
    return cleaned


def fallback_caption(evidence: EvidenceGraph, style: CaptionStyle) -> str:
    subject = _scene_subject(evidence).rstrip(".!? ")
    if style == "formal":
        return clean_caption(subject)
    if style == "sarcastic":
        return clean_caption(f"{subject}, making a routine moment look impressively official")
    if style == "humorous_tech":
        return clean_caption(f"{subject}, running the visible action like one very literal loop")
    return clean_caption(f"{subject}, turning the ordinary moment into a tiny performance")


def _caption_from_json(text: str) -> str | None:
    candidate = text
    if not candidate.startswith("{"):
        match = re.search(r"\{.*\}", candidate, flags=re.DOTALL)
        if not match:
            return None
        candidate = match.group(0)
    try:
        payload = json.loads(candidate)
    except (json.JSONDecodeError, TypeError):
        return None
    if isinstance(payload, dict) and isinstance(payload.get("caption"), str):
        return payload["caption"]
    return None


def _scene_subject(evidence: EvidenceGraph) -> str:
    candidates = [evidence.main_event, evidence.overall_summary]
    for segment in evidence.segments:
        candidates.extend(segment.observations)
    usable: list[str] = []
    for candidate in candidates:
        cleaned = _remove_artifact_language(candidate)
        if _is_generic_subject(cleaned) or not caption_is_usable(clean_caption(cleaned)):
            continue
        usable.append(cleaned)
    if usable:
        return min(usable, key=lambda value: len(value.split()))
    return "A visible scene unfolds in the video"


def _is_generic_subject(text: str) -> bool:
    lowered = text.strip().lower()
    return not lowered or lowered in {
        "a short video clip",
        "a short video clip is shown",
        "a video clip is shown",
        "the provided video",
    }


def _remove_artifact_language(text: str) -> str:
    cleaned = re.sub(
        r"(?i)^the image shows a contact sheet with .*?(?:\.\s+|$)",
        "",
        str(text),
    )
    cleaned = re.sub(r"(?i)^the (?:image|video|clip) (?:shows|depicts)\s+", "", cleaned)
    cleaned = re.sub(r"(?i)\b(?:frame|image)\s*F?\d+\b", "", cleaned)
    cleaned = re.sub(r"(?i)\bF\d{2}\b", "", cleaned)
    cleaned = re.sub(r"(?i)\b(?:across|in)\s+\d+\s+frames\b", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .,-")
    return cleaned
