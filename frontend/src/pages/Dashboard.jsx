import { useEffect, useState, useCallback } from "react";
import { useAuth } from "../context/AuthContext";
import { uploadResume, listResumes, analyzeResume, listAnalyses } from "../api/client";
import AnalysisResult from "../components/AnalysisResult";

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [resumes, setResumes] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState("");

  const refreshResumes = useCallback(async () => {
    try {
      const data = await listResumes();
      setResumes(data);
    } catch (err) {
      setError(err.message);
    }
  }, []);

  useEffect(() => {
    refreshResumes();
  }, [refreshResumes]);

  async function handleFileChange(e) {
    const file = e.target.files[0];
    if (!file) return;

    setError("");
    setUploading(true);
    try {
      const resume = await uploadResume(file);
      await refreshResumes();
      setSelectedId(resume.id);
      setAnalysis(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  }

  async function handleAnalyze(resumeId) {
    setError("");
    setAnalyzing(true);
    setAnalysis(null);
    try {
      const result = await analyzeResume(resumeId);
      setAnalysis(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setAnalyzing(false);
    }
  }

  async function handleSelectResume(resumeId) {
    setSelectedId(resumeId);
    setAnalysis(null);
    setError("");
    try {
      const analyses = await listAnalyses(resumeId);
      if (analyses.length > 0) setAnalysis(analyses[0]);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>AI Resume Analyzer</h1>
        <div className="user-info">
          <span>{user?.email}</span>
          <button onClick={logout} className="logout-btn">Log out</button>
        </div>
      </header>

      <section className="upload-section">
        <label className="upload-btn">
          {uploading ? "Uploading..." : "Upload Resume (PDF)"}
          <input type="file" accept="application/pdf" onChange={handleFileChange} disabled={uploading} hidden />
        </label>
        {error && <p className="error-text">{error}</p>}
      </section>

      <div className="dashboard-body">
        <aside className="resume-list">
          <h3>Your Resumes</h3>
          {resumes.length === 0 && <p className="muted">No resumes uploaded yet.</p>}
          <ul>
            {resumes.map((r) => (
              <li key={r.id} className={r.id === selectedId ? "selected" : ""} onClick={() => handleSelectResume(r.id)}>
                <span className="filename">{r.filename}</span>
                <span className={`status-badge ${r.status}`}>{r.status}</span>
              </li>
            ))}
          </ul>
        </aside>

        <main className="analysis-area">
          {selectedId ? (
            <>
              <button className="analyze-btn" onClick={() => handleAnalyze(selectedId)} disabled={analyzing}>
                {analyzing ? "Analyzing..." : "Run AI Analysis"}
              </button>
              {analysis && <AnalysisResult analysis={analysis} />}
            </>
          ) : (
            <p className="muted">Select or upload a resume to analyze it.</p>
          )}
        </main>
      </div>
    </div>
  );
}
