import React from "react";
import { Link } from "react-router-dom";

export function DashboardPage() {
  return (
    <div className="space-y-4">
      <div className="rounded-xl border border-slate-900 bg-slate-950 p-4">
        <div className="text-lg font-semibold">Welcome</div>
        <div className="text-slate-400 text-sm mt-1">
          Upload photos, label faces, and search naturally (e.g. “Show photos of Mom from last year”).
        </div>
        <div className="flex gap-3 mt-4">
          <Link to="/upload" className="px-4 py-2 rounded-md bg-indigo-600 hover:bg-indigo-500 font-medium">
            Upload photos
          </Link>
          <Link to="/gallery" className="px-4 py-2 rounded-md bg-slate-900 border border-slate-800 hover:bg-slate-800">
            Open gallery
          </Link>
        </div>
      </div>
    </div>
  );
}

