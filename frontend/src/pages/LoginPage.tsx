import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { login } from "../services/api";
import { useAuthStore } from "../store/auth";

export function LoginPage() {
  const nav = useNavigate();
  const setAuth = useAuthStore((s) => s.setAuth);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await login(email, password);
      setAuth(res.access_token, res.user);
      nav("/");
    } catch (err: any) {
      setError(err?.response?.data?.error ?? "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <div>
        <label className="block text-sm text-slate-300 mb-1">Email</label>
        <input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full bg-slate-950 border border-slate-800 rounded-md px-3 py-2 outline-none focus:border-slate-600"
          placeholder="you@example.com"
        />
      </div>
      <div>
        <label className="block text-sm text-slate-300 mb-1">Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full bg-slate-950 border border-slate-800 rounded-md px-3 py-2 outline-none focus:border-slate-600"
          placeholder="••••••••"
        />
      </div>
      {error && <div className="text-sm text-red-400">{error}</div>}
      <button
        disabled={loading}
        className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-60 rounded-md py-2 font-medium"
      >
        {loading ? "Signing in..." : "Sign in"}
      </button>
      <div className="text-sm text-slate-400">
        No account?{" "}
        <Link className="text-indigo-300 hover:underline" to="/register">
          Register
        </Link>
      </div>
    </form>
  );
}

