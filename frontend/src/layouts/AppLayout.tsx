import React from "react";
import { Link, Outlet, useLocation } from "react-router-dom";

import { ChatSidebar } from "../components/ChatSidebar";
import { useAuthStore } from "../store/auth";

const NavLink = ({ to, label }: { to: string; label: string }) => {
  const loc = useLocation();
  const active = loc.pathname === to;
  return (
    <Link
      to={to}
      className={[
        "px-3 py-2 rounded-md text-sm border",
        active ? "bg-slate-800 border-slate-700 text-white" : "border-transparent text-slate-300 hover:bg-slate-900 hover:border-slate-800"
      ].join(" ")}
    >
      {label}
    </Link>
  );
};

export function AppLayout() {
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);

  return (
    <div className="h-full bg-slate-950 text-slate-100">
      <div className="h-14 border-b border-slate-900 flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <div className="font-semibold">Drishyamitra</div>
          <div className="hidden md:flex items-center gap-2 ml-6">
            <NavLink to="/" label="Dashboard" />
            <NavLink to="/upload" label="Upload" />
            <NavLink to="/gallery" label="Gallery" />
            <NavLink to="/chat" label="Chat" />
            <NavLink to="/settings" label="Settings" />
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-xs text-slate-400">{user?.email}</div>
          <button
            onClick={logout}
            className="text-sm px-3 py-2 rounded-md bg-slate-900 border border-slate-800 hover:bg-slate-800"
          >
            Logout
          </button>
        </div>
      </div>

      <div className="flex h-[calc(100%-3.5rem)]">
        <main className="flex-1 overflow-auto p-4">
          <Outlet />
        </main>
        <aside className="hidden lg:block w-[380px] border-l border-slate-900">
          <ChatSidebar />
        </aside>
      </div>
    </div>
  );
}

