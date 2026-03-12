import React from "react";

import { useAuthStore } from "../store/auth";

export function SettingsPage() {
  const user = useAuthStore((s) => s.user);
  return (
    <div className="space-y-4">
      <div className="text-lg font-semibold">Settings</div>
      <div className="rounded-xl border border-slate-900 bg-slate-950 p-4">
        <div className="text-sm text-slate-300">Signed in as</div>
        <div className="text-sm text-slate-400 mt-1">{user?.email}</div>
      </div>
    </div>
  );
}

