import React, { useCallback, useState } from "react";

export function UploadDropzone({ onFiles }: { onFiles: (files: File[]) => void | Promise<void> }) {
  const [drag, setDrag] = useState(false);

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDrag(false);
      const files = Array.from(e.dataTransfer.files).filter((f) => f.type.startsWith("image/"));
      if (files.length) onFiles(files);
    },
    [onFiles]
  );

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setDrag(true);
      }}
      onDragLeave={() => setDrag(false)}
      onDrop={onDrop}
      className={[
        "rounded-xl border border-dashed p-10 text-center transition",
        drag ? "border-indigo-400 bg-indigo-950/30" : "border-slate-800 bg-slate-950"
      ].join(" ")}
    >
      <div className="text-sm text-slate-300">Drop images here</div>
      <div className="text-xs text-slate-500 mt-1">PNG/JPG/WEBP</div>
      <div className="mt-4">
        <label className="inline-flex items-center px-4 py-2 rounded-md bg-slate-900 border border-slate-800 hover:bg-slate-800 cursor-pointer text-sm">
          Select file
          <input
            className="hidden"
            type="file"
            accept="image/*"
            onChange={(e) => {
              const f = e.target.files?.[0];
              if (f) onFiles([f]);
            }}
          />
        </label>
      </div>
    </div>
  );
}

