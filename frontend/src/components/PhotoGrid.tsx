import React from "react";

export function PhotoGrid({ photoIds }: { photoIds: number[] }) {
  if (!photoIds.length) {
    return <div className="text-sm text-slate-500">No photos yet.</div>;
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-3">
      {photoIds.map((id) => (
        <div key={id} className="rounded-lg overflow-hidden border border-slate-900 bg-slate-950">
          <img className="w-full h-48 object-cover" src={`/api/photos/${id}/file`} alt={`Photo ${id}`} />
          <div className="px-3 py-2 text-xs text-slate-400">
            <span className="font-mono">#{id}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

