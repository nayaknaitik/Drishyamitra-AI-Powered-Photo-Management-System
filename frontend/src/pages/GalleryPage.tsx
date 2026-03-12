import React, { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { listPhotos, search } from "../services/api";
import { PhotoGrid } from "../components/PhotoGrid";

export function GalleryPage() {
  const [q, setQ] = useState("");
  const photosQ = useQuery({ queryKey: ["photos"], queryFn: listPhotos });
  const [searchResult, setSearchResult] = useState<any | null>(null);

  const items = useMemo(() => {
    if (searchResult?.items) return searchResult.items;
    return photosQ.data?.items ?? [];
  }, [photosQ.data, searchResult]);

  async function runSearch(e: React.FormEvent) {
    e.preventDefault();
    if (!q.trim()) {
      setSearchResult(null);
      return;
    }
    const res = await search(q);
    setSearchResult(res);
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-lg font-semibold">Gallery</div>
          <div className="text-sm text-slate-400">Natural language search works best after labeling faces.</div>
        </div>
      </div>

      <form onSubmit={runSearch} className="flex gap-2">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          className="flex-1 bg-slate-950 border border-slate-800 rounded-md px-3 py-2 outline-none focus:border-slate-600"
          placeholder='Try: "Show photos of Mom from last year"'
        />
        <button className="px-4 py-2 rounded-md bg-slate-900 border border-slate-800 hover:bg-slate-800 text-sm">
          Search
        </button>
      </form>

      {photosQ.isLoading && <div className="text-sm text-slate-400">Loading…</div>}
      {photosQ.error && <div className="text-sm text-red-400">Failed to load photos</div>}

      <PhotoGrid photoIds={items.map((p: any) => p.id)} />
    </div>
  );
}

