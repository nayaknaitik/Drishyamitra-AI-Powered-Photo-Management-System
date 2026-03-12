import React, { useState } from "react";

import { FaceLabelModal } from "../components/FaceLabelModal";
import { UploadDropzone } from "../components/UploadDropzone";
import { uploadPhoto } from "../services/api";

export function UploadPage() {
  const [lastUpload, setLastUpload] = useState<{ photo_id: number; faces: any[] } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onFiles(files: File[]) {
    setError(null);
    setBusy(true);
    try {
      // MVP: upload first file only
      const res = await uploadPhoto(files[0]);
      setLastUpload(res);
    } catch (e: any) {
      setError(e?.response?.data?.error ?? "Upload failed");
    } finally {
      setBusy(false);
    }
  }

  const unknownFaces = (lastUpload?.faces ?? []).filter((f) => f.is_unknown);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-lg font-semibold">Upload</div>
          <div className="text-sm text-slate-400">Drag and drop an image. We’ll detect faces and prompt labeling.</div>
        </div>
        {busy && <div className="text-sm text-slate-400">Processing…</div>}
      </div>

      <UploadDropzone onFiles={onFiles} />
      {error && <div className="text-sm text-red-400">{error}</div>}

      {lastUpload && (
        <div className="rounded-xl border border-slate-900 bg-slate-950 p-4">
          <div className="text-sm text-slate-300">
            Uploaded photo <span className="font-mono">#{lastUpload.photo_id}</span> — detected{" "}
            <span className="font-semibold">{lastUpload.faces.length}</span> face(s).
          </div>
        </div>
      )}

      {lastUpload && unknownFaces.length > 0 && (
        <FaceLabelModal
          faces={unknownFaces}
          onDone={() => {
            // For now just close modal state by clearing unknowns
            setLastUpload({ ...lastUpload, faces: lastUpload.faces.map((f) => ({ ...f, is_unknown: false })) });
          }}
        />
      )}
    </div>
  );
}

