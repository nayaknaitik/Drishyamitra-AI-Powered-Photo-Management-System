import React from "react";
import { Outlet } from "react-router-dom";

export function AuthLayout() {
  return (
    <div className="min-h-full bg-slate-950 text-slate-100 flex items-center justify-center p-6">
      <div className="w-full max-w-md rounded-xl bg-slate-900 border border-slate-800 p-6">
        <div className="mb-6">
          <div className="text-xl font-semibold">Drishyamitra</div>
          <div className="text-sm text-slate-400">AI-powered photo management</div>
        </div>
        <Outlet />
      </div>
    </div>
  );
}

