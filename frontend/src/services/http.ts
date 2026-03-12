import axios from "axios";

import { useAuthStore } from "../store/auth";

export const http = axios.create({
  baseURL: "/api",
  timeout: 30000
});

http.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

