import React from "react";

import { ChatSidebar } from "../components/ChatSidebar";

export function ChatPage() {
  return (
    <div className="h-[calc(100vh-3.5rem-2rem)] rounded-xl border border-slate-900 overflow-hidden">
      <ChatSidebar />
    </div>
  );
}

