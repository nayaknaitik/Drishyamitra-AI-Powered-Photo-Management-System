import { http } from "./http";

export type AuthResponse = { user: { id: number; email: string }; access_token: string };

export async function register(email: string, password: string): Promise<AuthResponse> {
  const { data } = await http.post<AuthResponse>("/auth/register", { email, password });
  return data;
}

export async function login(email: string, password: string): Promise<AuthResponse> {
  const { data } = await http.post<AuthResponse>("/auth/login", { email, password });
  return data;
}

export type PhotoListItem = { id: number; taken_at: string | null; created_at: string; original_filename: string | null };

export async function listPhotos(): Promise<{ items: PhotoListItem[] }> {
  const { data } = await http.get<{ items: PhotoListItem[] }>("/photos");
  return data;
}

export type UploadFace = {
  id: number;
  x: number;
  y: number;
  w: number;
  h: number;
  is_unknown: boolean;
  person_id: number | null;
  person_name: string | null;
};

export async function uploadPhoto(file: File): Promise<{ photo_id: number; faces: UploadFace[] }> {
  const form = new FormData();
  form.append("file", file);
  const { data } = await http.post("/photos/upload", form, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return data as { photo_id: number; faces: UploadFace[] };
}

export async function labelFace(face_id: number, person_name: string): Promise<{ face: { id: number; person_id: number; is_unknown: boolean } }> {
  const { data } = await http.post("/faces/label", { face_id, person_name });
  return data;
}

export async function listPersons(): Promise<{ items: { id: number; name: string }[] }> {
  const { data } = await http.get("/faces/persons");
  return data;
}

export async function search(query: string): Promise<any> {
  const { data } = await http.post("/search", { query });
  return data;
}

export async function chat(message: string): Promise<any> {
  const { data } = await http.post("/chat", { message });
  return data;
}

