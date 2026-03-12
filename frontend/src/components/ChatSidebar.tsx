import React, { useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { chat } from "../services/api";

type Msg = { role: "user" | "assistant"; text: string };

export function ChatSidebar() {
  const [messages, setMessages] = useState<Msg[]>([
    { role: "assistant", text: "Ask me things like: “show photos of mom”, “find pictures of Priya at Diwali”." }
  ]);
  const [text, setText] = useState("");

  const m = useMutation({
    mutationFn: (msg: string) => chat(msg),
    onSuccess: (data) => {
      setMessages((prev) => [...prev, { role: "assistant", text: data.reply ?? JSON.stringify(data) }]);
    },
    onError: () => {
      setMessages((prev) => [...prev, { role: "assistant", text: "Sorry — chat failed." }]);
    }
  });

  function send() {
    const msg = text.trim();
    if (!msg) return;
    setMessages((prev) => [...prev, { role: "user", text: msg }]);
    setText("");
    m.mutate(msg);
  }

  return (
    <div className="h-full flex flex-col">
      <div className="px-4 py-3 border-b border-slate-900">
        <div className="font-semibold">Assistant</div>
        <div className="text-xs text-slate-500">Groq-powered when configured</div>
      </div>
      <div className="flex-1 overflow-auto p-4 space-y-3">
        {messages.map((m, i) => (
          <div
            key={i}
            className={[
              "text-sm rounded-lg px-3 py-2 border",
              m.role === "user" ? "ml-8 bg-slate-900 border-slate-800" : "mr-8 bg-slate-950 border-slate-900"
            ].join(" ")}
          >
            <div className="text-xs text-slate-500 mb-1">{m.role}</div>
            <div className="text-slate-200 whitespace-pre-wrap">{m.text}</div>
          </div>
        ))}
      </div>
      <div className="p-3 border-t border-slate-900">
        <div className="flex gap-2">
          <input
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") send();
            }}
            className="flex-1 bg-slate-950 border border-slate-800 rounded-md px-3 py-2 outline-none focus:border-slate-600 text-sm"
            placeholder="Ask…"
          />
          <button
            onClick={send}
            disabled={m.isPending}
            className="px-3 py-2 rounded-md bg-indigo-600 hover:bg-indigo-500 disabled:opacity-60 text-sm font-medium"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

