import React, { useMemo } from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { listPersons, search } from "../services/api";
import { PhotoGrid } from "../components/PhotoGrid";

export function PersonViewPage() {
  const { id } = useParams();
  const personId = Number(id);

  const personsQ = useQuery({ queryKey: ["persons"], queryFn: listPersons });
  const person = useMemo(() => personsQ.data?.items.find((p) => p.id === personId), [personsQ.data, personId]);

  const photosQ = useQuery({
    queryKey: ["person-photos", person?.name],
    queryFn: () => search(`photos of ${person?.name ?? ""}`),
    enabled: !!person?.name
  });

  const photoIds: number[] = (photosQ.data?.items ?? []).map((p: any) => p.id);

  return (
    <div className="space-y-4">
      <div>
        <div className="text-lg font-semibold">{person?.name ?? "Person"}</div>
        <div className="text-sm text-slate-400">Photos automatically organized by face recognition.</div>
      </div>

      {photosQ.isLoading && <div className="text-sm text-slate-400">Loading…</div>}
      {photosQ.error && <div className="text-sm text-red-400">Failed to load person photos</div>}

      <PhotoGrid photoIds={photoIds} />
    </div>
  );
}

