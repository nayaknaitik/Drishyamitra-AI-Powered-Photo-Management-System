import React, { useMemo, useState } from "react";

import { labelFace } from "../services/api";

export function FaceLabelModal({
  faces,
  onDone
}: {
  faces: { id: number; x: number; y: number; w: number; h: number }[];
  onDone: () => void;
}) {
  const [idx, setIdx] = useState(0);
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const face = faces[idx];
  const remaining = useMemo(() => faces.length - idx, [faces.length, idx]);

  async function submit() {
    setError(null);
    setBusy(true);
    try {
      await labelFace(face.id, name);
      setName("");
      if (idx + 1 >= faces.length) onDone();
      else setIdx(idx + 1);
    } catch (e: any) {
      setError(e?.response?.data?.error ?? "Label failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4">
      <div className="w-full max-w-lg rounded-xl bg-slate-950 border border-slate-800 p-5">
        <div className="flex items-center justify-between">
          <div>
            <div className="font-semibold">Label faces</div>
            <div className="text-xs text-slate-500">{remaining} remaining</div>
          </div>
          <button onClick={onDone} className="text-sm text-slate-400 hover:text-slate-200">
            Close
          </button>
        </div>

        <div className="mt-4 text-sm text-slate-300">
          Face <span className="font-mono">#{face.id}</span> — enter the person’s name.
        </div>

        <div className="mt-3">
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-md px-3 py-2 outline-none focus:border-slate-600"
            placeholder="e.g. Mom, Priya, John"
          />
        </div>

        {error && <div className="text-sm text-red-400 mt-2">{error}</div>}

        <div className="mt-4 flex gap-2 justify-end">
          <button
            onClick={onDone}
            className="px-4 py-2 rounded-md bg-slate-900 border border-slate-800 hover:bg-slate-800 text-sm"
          >
            Skip
          </button>
          <button
            disabled={busy || !name.trim()}
            onClick={submit}
            className="px-4 py-2 rounded-md bg-indigo-600 hover:bg-indigo-500 disabled:opacity-60 text-sm font-medium"
          >
            {busy ? "Saving..." : "Save label"}
          </button>
        </div>
      </div>
    </div>
  );
}

