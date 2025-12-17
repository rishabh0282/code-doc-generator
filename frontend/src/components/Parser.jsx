import React, { useState } from "react";
import "./Parser.css";

export default function Parser() {
  const [path, setPath] = useState("");
  const [type, setType] = useState("file"); // "file" or "directory"
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(e) {
    e.preventDefault();
    if (!path.trim()) {
      setError("Please enter a path");
      return;
    }
    setLoading(true);
    setError("");
    const endpoint = type === "file" ? "/api/parse-file" : "/api/parse-directory";
    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path }),
      });
      const json = await res.json();
      if (res.ok) {
        setResult(json);
      } else {
        setError(json.detail || "Parse failed");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="parser-container">
      <h2>?? Parse Code</h2>
      <form onSubmit={submit}>
        <div className="form-group">
          <label>Type:</label>
          <select value={type} onChange={(e) => setType(e.target.value)} disabled={loading}>
            <option value="file">Single File</option>
            <option value="directory">Directory</option>
          </select>
        </div>
        <div className="form-group">
          <input
            value={path}
            onChange={(e) => setPath(e.target.value)}
            placeholder={type === "file" ? "path/to/file.py" : "path/to/directory"}
            disabled={loading}
          />
        </div>
        <button type="submit" disabled={loading || !path.trim()}>
          {loading ? "Parsing..." : "Parse"}
        </button>
      </form>
      {error && <div className="error-message">{error}</div>}
      {loading && <div className="loading">Processing code...</div>}
      {result && (
        <div className="result-box">
          <h3>Results</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
