"use client";

import {
  AlertTriangle,
  CheckCircle2,
  Clapperboard,
  Download,
  FileVideo,
  FolderPlus,
  Loader2,
  Play,
  Plus,
  ScrollText,
  Trash2,
  Upload,
} from "lucide-react";
import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import { toast } from "sonner";

type CaptionMap = {
  formal?: string;
  sarcastic?: string;
  humorous_tech?: string;
  humorous_non_tech?: string;
};

type QueueItem = {
  id: string;
  kind: "url" | "upload";
  title: string;
  description: string;
  file?: File;
  videoUrl?: string;
  previewUrl?: string;
  status: "pending" | "running" | "complete" | "failed";
  runId?: string;
  error?: string;
  elapsedSec?: number;
  captions?: CaptionMap;
  restored?: boolean;
};

type PersistedQueueItem = Omit<QueueItem, "file" | "previewUrl"> & {
  previewUrl?: string;
};

type PersistedWorkbench = {
  activeItemId: string | null;
  items: PersistedQueueItem[];
};

const STYLE_LABELS: Array<[keyof CaptionMap, string]> = [
  ["formal", "Formal"],
  ["sarcastic", "Sarcastic"],
  ["humorous_tech", "Humorous tech"],
  ["humorous_non_tech", "Humorous non-tech"],
];

const STORAGE_KEY = "captionman.studio.workbench.v1";

export function RunLauncherPanel() {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const previewUrlsRef = useRef<Set<string>>(new Set());
  const [items, setItems] = useState<QueueItem[]>([]);
  const [activeItemId, setActiveItemId] = useState<string | null>(null);
  const [hydrated, setHydrated] = useState(false);
  const [sceneHint, setSceneHint] = useState("");
  const [videoUrl, setVideoUrl] = useState("");

  const activeItem = useMemo(
    () => items.find((item) => item.id === activeItemId) ?? items[0],
    [activeItemId, items],
  );
  const pendingCount = items.filter((item) => item.status === "pending").length;
  const running = items.some((item) => item.status === "running");

  useEffect(() => {
    const restored = restoreWorkbench();
    if (restored) {
      setItems(restored.items);
      setActiveItemId(restored.activeItemId);
    }
    setHydrated(true);
    return () => {
      for (const previewUrl of previewUrlsRef.current) {
        URL.revokeObjectURL(previewUrl);
      }
      previewUrlsRef.current.clear();
    };
  }, []);

  useEffect(() => {
    if (!hydrated) {
      return;
    }
    persistWorkbench(items, activeItem?.id ?? null);
  }, [hydrated, items, activeItem?.id]);

  function addUrl() {
    const trimmed = videoUrl.trim();
    if (!trimmed) {
      toast.error("Paste a video URL first");
      return;
    }
    if (!/^https?:\/\//i.test(trimmed)) {
      toast.error("Use a direct http or https video URL");
      return;
    }
    const item: QueueItem = {
      id: `url-${Date.now()}-${crypto.randomUUID()}`,
      kind: "url",
      title: titleFromUrl(trimmed),
      description: sceneHint.trim(),
      videoUrl: trimmed,
      previewUrl: trimmed,
      status: "pending",
    };
    setItems((current) => [item, ...current]);
    setActiveItemId(item.id);
    setVideoUrl("");
    setSceneHint("");
  }

  function addFiles(files: FileList | null) {
    if (!files?.length) {
      return;
    }
    const nextItems = Array.from(files).map((file) => {
      const previewUrl = URL.createObjectURL(file);
      previewUrlsRef.current.add(previewUrl);
      return {
        id: `upload-${Date.now()}-${crypto.randomUUID()}`,
        kind: "upload" as const,
        title: file.name,
        description: sceneHint.trim(),
        file,
        previewUrl,
        status: "pending" as const,
      };
    });
    setItems((current) => [...nextItems, ...current]);
    setActiveItemId(nextItems[0]?.id ?? null);
    setSceneHint("");
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }

  function removeItem(id: string) {
    setItems((current) => {
      const removed = current.find((item) => item.id === id);
      if (removed?.previewUrl) {
        URL.revokeObjectURL(removed.previewUrl);
        previewUrlsRef.current.delete(removed.previewUrl);
      }
      return current.filter((item) => item.id !== id);
    });
    if (activeItemId === id) {
      setActiveItemId(null);
    }
  }

  async function runPending() {
    if (running || pendingCount === 0) {
      return;
    }
    for (const item of items.filter((entry) => entry.status === "pending")) {
      await runOne(item);
    }
  }

  async function rerun(id: string) {
    const item = items.find((entry) => entry.id === id);
    if (!item || running) {
      return;
    }
    await runOne({
      ...item,
      status: "pending",
      error: undefined,
      captions: undefined,
    });
  }

  async function runOne(item: QueueItem) {
    const base =
      process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
    const startedAt = Date.now();
    updateItem(item.id, {
      status: "running",
      error: undefined,
      elapsedSec: 0,
      captions: undefined,
    });
    setActiveItemId(item.id);
    try {
      const payload =
        item.kind === "url"
          ? await startUrlRun(base, item)
          : await startUploadRun(base, item);
      if (!payload.run_id) {
        throw new Error("API did not return run_id");
      }
      updateItem(item.id, { runId: payload.run_id });
      await waitForRunComplete(base, payload.run_id, (elapsedSec) => {
        updateItem(item.id, { elapsedSec });
      });
      const captions = await fetchFirstCaptionResult(base, payload.run_id);
      updateItem(item.id, {
        status: "complete",
        runId: payload.run_id,
        captions,
        elapsedSec: Math.round((Date.now() - startedAt) / 1000),
      });
      toast.success("Caption run complete", { description: item.title });
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown error";
      updateItem(item.id, { status: "failed", error: message });
      toast.error("Caption run failed", { description: message });
    }
  }

  function updateItem(id: string, patch: Partial<QueueItem>) {
    setItems((current) =>
      current.map((entry) =>
        entry.id === id ? { ...entry, ...patch } : entry,
      ),
    );
  }

  return (
    <section className="cm-workbench" aria-label="Caption workbench">
      <div className="cm-panel cm-source-panel p-5">
        <div className="flex items-start justify-between gap-3">
          <div>
            <span className="cm-kicker">
              <FolderPlus size={15} />
              Sources
            </span>
            <h2 className="mt-3 text-2xl font-semibold">Add videos</h2>
          </div>
          <span className="cm-chip">{items.length} queued</span>
        </div>

        <div className="mt-5 grid gap-3">
          <label className="cm-field">
            <span>Direct video URL</span>
            <input
              onChange={(event) => setVideoUrl(event.target.value)}
              placeholder="https://storage.googleapis.com/.../clip.mp4"
              value={videoUrl}
            />
          </label>
          <label className="cm-field">
            <span>Scene hint</span>
            <input
              onChange={(event) => setSceneHint(event.target.value)}
              placeholder="Optional"
              value={sceneHint}
            />
          </label>
          <button
            className="cm-button cm-button-primary"
            onClick={addUrl}
            type="button"
          >
            <Download size={16} />
            Add URL
          </button>
          <button
            className="cm-button"
            onClick={() => fileInputRef.current?.click()}
            type="button"
          >
            <Upload size={16} />
            Add video files
          </button>
          <input
            ref={fileInputRef}
            aria-label="Upload videos"
            accept="video/mp4,video/quicktime,video/x-msvideo,video/x-matroska,video/webm"
            className="sr-only"
            multiple
            onChange={(event) => addFiles(event.target.files)}
            type="file"
          />
        </div>

        <div className="cm-divider my-5" />

        <button
          className="cm-button cm-button-primary w-full"
          disabled={running || pendingCount === 0}
          onClick={runPending}
          type="button"
        >
          {running ? (
            <Loader2 className="animate-spin" size={16} />
          ) : (
            <Play size={16} />
          )}
          {running
            ? "Captioning in progress"
            : pendingCount > 0
              ? `Run ${pendingCount} pending`
              : "Nothing pending"}
        </button>
        <Link className="cm-button mt-3 w-full" href="/submission">
          <ScrollText size={16} />
          Docker readiness
        </Link>
      </div>

      <div className="cm-panel p-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <span className="cm-kicker">
            <FileVideo size={15} />
            Queue
          </span>
          <span className="cm-chip cm-chip-gold">
            <AlertTriangle size={14} />
            Uses active provider
          </span>
        </div>

        {items.length ? (
          <div className="cm-video-list mt-5">
            {items.map((item) => (
              <button
                aria-pressed={activeItem?.id === item.id}
                className="cm-video-row"
                key={item.id}
                onClick={() => setActiveItemId(item.id)}
                type="button"
              >
                <span className="cm-video-thumb">
                  {item.previewUrl ? (
                    <video muted preload="metadata" src={item.previewUrl} />
                  ) : (
                    <Clapperboard size={20} />
                  )}
                </span>
                <span className="min-w-0 flex-1 text-left">
                  <strong>{item.title}</strong>
                  <small>{item.description || "All four caption styles"}</small>
                </span>
                <StatusPill item={item} />
              </button>
            ))}
          </div>
        ) : (
          <div className="cm-empty-state mt-5">
            <Plus size={26} />
            <p>Paste a video URL or upload files to start.</p>
          </div>
        )}
      </div>

      <div className="cm-panel p-5">
        <span className="cm-kicker">
          <ScrollText size={15} />
          Result
        </span>
        {activeItem ? (
          <ResultCard
            item={activeItem}
            onRemove={removeItem}
            onRerun={rerun}
            running={running}
          />
        ) : (
          <div className="cm-empty-state mt-5">
            <ScrollText size={26} />
            <p>Select a completed run to review captions.</p>
          </div>
        )}
      </div>
    </section>
  );
}

function ResultCard({
  item,
  onRemove,
  onRerun,
  running,
}: {
  item: QueueItem;
  onRemove: (id: string) => void;
  onRerun: (id: string) => void;
  running: boolean;
}) {
  return (
    <div className="mt-5 grid gap-4">
      <div className="cm-preview-stage">
        {item.previewUrl ? (
          <video controls preload="metadata" src={item.previewUrl}>
            <track
              default
              kind="captions"
              label="No captions available"
              src="data:text/vtt,WEBVTT"
            />
          </video>
        ) : (
          <div className="cm-preview-placeholder">
            <Clapperboard size={32} />
            <span>{item.title}</span>
          </div>
        )}
      </div>

      <div className="flex flex-wrap gap-2">
        <button
          className="cm-button"
          disabled={
            running ||
            item.status === "running" ||
            (item.kind === "upload" && !item.file)
          }
          onClick={() => onRerun(item.id)}
          type="button"
        >
          {item.status === "running" ? (
            <Loader2 className="animate-spin" size={16} />
          ) : (
            <Play size={16} />
          )}
          Run again
        </button>
        {item.runId ? (
          <Link
            className="cm-button cm-button-primary"
            href={`/runs/${item.runId}`}
            prefetch={false}
          >
            <ScrollText size={16} />
            Open Judge Verdict
          </Link>
        ) : null}
        <button
          className="cm-button"
          onClick={() => onRemove(item.id)}
          type="button"
        >
          <Trash2 size={16} />
          Remove
        </button>
      </div>

      {item.status === "running" ? (
        <div className="cm-panel-soft p-4">
          <p className="font-semibold">Captioning {item.title}</p>
          <p className="cm-muted mt-1 text-sm">
            {item.runId ? `${item.runId} - ` : ""}
            {formatElapsed(item.elapsedSec ?? 0)} elapsed
          </p>
          <div className="cm-run-progress mt-4">
            <span />
          </div>
        </div>
      ) : null}

      {item.kind === "upload" && item.restored && !item.file ? (
        <div className="cm-panel-soft p-4">
          <p className="font-semibold">Restored completed upload</p>
          <p className="cm-muted mt-1 text-sm">
            Captions and Judge Verdict are preserved. Re-upload the source file
            if you want to run it again.
          </p>
        </div>
      ) : null}

      {item.status === "failed" ? (
        <div className="cm-panel-soft border-[rgba(228,90,114,0.38)] p-4">
          <p className="font-semibold text-[var(--cm-risk-ruby)]">Run failed</p>
          <p className="cm-muted mt-1 text-sm">{item.error}</p>
        </div>
      ) : null}

      {item.captions ? (
        <div className="grid gap-3">
          {STYLE_LABELS.map(([key, label]) => (
            <div className="cm-caption-card" key={key}>
              <span>{label}</span>
              <p>{item.captions?.[key] || "No caption returned."}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="cm-panel-soft p-4">
          <p className="font-semibold">No captions yet.</p>
          <p className="cm-muted mt-1 text-sm">
            Run this source to generate formal, sarcastic, humorous tech, and
            humorous non-tech captions.
          </p>
        </div>
      )}
    </div>
  );
}

function StatusPill({ item }: { item: QueueItem }) {
  if (item.status === "complete") {
    return (
      <span className="cm-chip cm-chip-teal">
        <CheckCircle2 size={14} />
        Done
      </span>
    );
  }
  if (item.status === "failed") {
    return (
      <span className="cm-chip cm-chip-ruby">
        <AlertTriangle size={14} />
        Failed
      </span>
    );
  }
  if (item.status === "running") {
    return (
      <span className="cm-chip cm-chip-gold">
        <Loader2 className="animate-spin" size={14} />
        Running
      </span>
    );
  }
  return <span className="cm-chip">Pending</span>;
}

async function startUrlRun(
  base: string,
  item: QueueItem,
): Promise<{ run_id?: string }> {
  if (!item.videoUrl) {
    throw new Error("Missing video URL");
  }
  const response = await fetch(`${base}/api/runs/url`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      video_url: item.videoUrl,
      task_id: safeTaskId(item.title),
      description: item.description,
    }),
  });
  if (!response.ok) {
    throw new Error(`URL API returned ${response.status}`);
  }
  return response.json();
}

async function startUploadRun(
  base: string,
  item: QueueItem,
): Promise<{ run_id?: string }> {
  if (!item.file) {
    throw new Error("Missing video file");
  }
  const body = new FormData();
  body.set("video", item.file);
  body.set("task_id", safeTaskId(item.title));
  body.set("description", item.description);
  const response = await fetch(`${base}/api/runs/upload`, {
    method: "POST",
    body,
  });
  if (!response.ok) {
    throw new Error(`Upload API returned ${response.status}`);
  }
  return response.json();
}

async function waitForRunComplete(
  base: string,
  runId: string,
  onProgress?: (elapsedSec: number) => void,
) {
  const startedAt = Date.now();
  for (let attempt = 0; attempt < 330; attempt += 1) {
    const elapsedSec = Math.round((Date.now() - startedAt) / 1000);
    onProgress?.(elapsedSec);
    const response = await fetch(`${base}/api/runs/${runId}`, {
      cache: "no-store",
    });
    if (!response.ok) {
      throw new Error(`Status check returned ${response.status}`);
    }
    const payload = (await response.json()) as {
      status?: string;
      error?: string;
    };
    if (payload.status === "complete") {
      return;
    }
    if (payload.status === "failed") {
      throw new Error(payload.error ?? "Run failed");
    }
    await new Promise((resolve) => setTimeout(resolve, 2000));
  }
  throw new Error("The run is still processing after 11 minutes.");
}

async function fetchFirstCaptionResult(
  base: string,
  runId: string,
): Promise<CaptionMap> {
  const response = await fetch(`${base}/api/runs/${runId}/artifacts/results`, {
    cache: "no-store",
  });
  if (!response.ok) {
    return {};
  }
  const payload = await response.json();
  const first = Array.isArray(payload) ? payload[0] : payload;
  return first?.captions ?? {};
}

function formatElapsed(seconds: number) {
  const minutes = Math.floor(seconds / 60);
  const rest = seconds % 60;
  return `${minutes}:${String(rest).padStart(2, "0")}`;
}

function safeTaskId(name: string) {
  return (
    name
      .replace(/\.[^.]+$/, "")
      .toLowerCase()
      .replace(/[^a-z0-9_-]+/g, "-")
      .replace(/^-|-$/g, "")
      .slice(0, 48) || "uploaded-video"
  );
}

function titleFromUrl(url: string) {
  try {
    const parsed = new URL(url);
    const filename = parsed.pathname.split("/").filter(Boolean).at(-1);
    return filename || parsed.hostname;
  } catch {
    return "video-url";
  }
}

function restoreWorkbench(): PersistedWorkbench | null {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return null;
    }
    const parsed = JSON.parse(raw) as PersistedWorkbench;
    if (!Array.isArray(parsed.items)) {
      return null;
    }
    const items = parsed.items
      .filter((item) => item.id && item.title)
      .map((item) => ({
        ...item,
        previewUrl: item.kind === "url" ? item.videoUrl : undefined,
        status: item.status === "running" ? "failed" : item.status,
        error:
          item.status === "running"
            ? "Run was interrupted when the Studio page was restored."
            : item.error,
        restored: item.kind === "upload",
      }));
    return {
      activeItemId:
        parsed.activeItemId &&
        items.some((item) => item.id === parsed.activeItemId)
          ? parsed.activeItemId
          : (items[0]?.id ?? null),
      items,
    };
  } catch {
    return null;
  }
}

function persistWorkbench(items: QueueItem[], activeItemId: string | null) {
  try {
    const persistedItems = items
      .filter((item) => item.status !== "pending" || item.kind === "url")
      .slice(0, 24)
      .map((item) => ({
        id: item.id,
        kind: item.kind,
        title: item.title,
        description: item.description,
        videoUrl: item.videoUrl,
        previewUrl: item.kind === "url" ? item.videoUrl : undefined,
        status: item.status,
        runId: item.runId,
        error: item.error,
        elapsedSec: item.elapsedSec,
        captions: item.captions,
      }));
    window.localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ activeItemId, items: persistedItems }),
    );
  } catch {
    // Storage can fail in private browsing or quota-limited contexts.
  }
}
