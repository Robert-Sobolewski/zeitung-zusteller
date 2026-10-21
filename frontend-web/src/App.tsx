import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8080";

interface HealthResponse {
  status: string;
  service: string;
  database: string;
}

export default function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_URL}/api/health`)
      .then((r) => r.json())
      .then(setHealth)
      .catch((e: Error) => setError(e.message));
  }, []);

  return (
    <main style={{ fontFamily: "system-ui, sans-serif", padding: "2rem" }}>
      <h1>ZeitungsZusteller Platform</h1>
      {error && <p role="alert">Backend offline: {error}</p>}
      {health && (
        <ul>
          <li>Status: {health.status}</li>
          <li>Baza danych: {health.database}</li>
        </ul>
      )}
    </main>
  );
}
