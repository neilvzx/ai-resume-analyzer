const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function getToken() {
  return localStorage.getItem("access_token");
}

async function request(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });

  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch {
      // response wasn't JSON, keep default message
    }
    throw new Error(detail);
  }

  if (res.status === 204) return null;
  return res.json();
}

export async function registerUser({ email, password, full_name }) {
  return request("/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, full_name }),
  });
}

export async function loginUser({ email, password }) {
  const body = new URLSearchParams();
  body.set("username", email);
  body.set("password", password);

  const res = await fetch(`${BASE_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });

  if (!res.ok) {
    let detail = "Login failed";
    try {
      const b = await res.json();
      detail = b.detail || detail;
    } catch {
      /* noop */
    }
    throw new Error(detail);
  }

  const data = await res.json();
  localStorage.setItem("access_token", data.access_token);
  return data;
}

export function logoutUser() {
  localStorage.removeItem("access_token");
}

export async function getCurrentUser() {
  return request("/api/auth/me");
}

export async function uploadResume(file) {
  const formData = new FormData();
  formData.append("file", file);

  return request("/api/resumes/upload", {
    method: "POST",
    body: formData,
  });
}

export async function listResumes() {
  return request("/api/resumes/");
}

export async function getResume(resumeId) {
  return request(`/api/resumes/${resumeId}`);
}

export async function analyzeResume(resumeId) {
  return request(`/api/resumes/${resumeId}/analyze`, { method: "POST" });
}

export async function listAnalyses(resumeId) {
  return request(`/api/resumes/${resumeId}/analyses`);
}
