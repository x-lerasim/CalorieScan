const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:4000";

export async function analyzeImage(file, portion) {
  const formData = new FormData();
  formData.append("image", file);
  if (portion !== undefined && portion !== null && portion !== "") {
    formData.append("portion", String(portion));
  }

  const response = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.error || `Request failed with status ${response.status}`);
  }

  return response.json();
}

export async function fetchHealth() {
  const response = await fetch(`${API_BASE}/api/health`);
  if (!response.ok) throw new Error("API unavailable");
  return response.json();
}
