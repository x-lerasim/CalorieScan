import React, { useEffect, useMemo, useState } from "react";
import ImageUpload from "./components/ImageUpload.jsx";
import Results from "./components/Results.jsx";
import { analyzeImage } from "./api.js";

export default function App() {
  const [file, setFile] = useState(null);
  const [portion, setPortion] = useState(200);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const previewUrl = useMemo(() => (file ? URL.createObjectURL(file) : null), [file]);

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const handleFileChange = (picked) => {
    setFile(picked);
    setData(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Сначала выберите фото");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const result = await analyzeImage(file, portion);
      setData(result);
    } catch (err) {
      setError(err.message || "Не удалось проанализировать изображение");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setData(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>
          <span className="logo">🥗</span> CalorieScan
        </h1>
        <p>AI-счётчик калорий по фото</p>
      </header>

      <main className="main">
        <section className="panel">
          <ImageUpload
            file={file}
            previewUrl={previewUrl}
            onFileChange={handleFileChange}
            disabled={loading}
          />

          <div className="controls">
            <label htmlFor="portion">
              Размер порции: <strong>{portion} г</strong>
            </label>
            <input
              id="portion"
              type="range"
              min="50"
              max="500"
              step="50"
              value={portion}
              onChange={(e) => setPortion(Number(e.target.value))}
              disabled={loading}
            />

            <div className="buttons">
              <button
                type="button"
                className="primary"
                onClick={handleAnalyze}
                disabled={loading || !file}
              >
                {loading ? "Анализирую..." : "Проанализировать"}
              </button>
              <button
                type="button"
                className="secondary"
                onClick={handleReset}
                disabled={loading}
              >
                Сбросить
              </button>
            </div>

            {error && (
              <div className="error" role="alert">
                {error}
              </div>
            )}
          </div>
        </section>

        <section className="panel">
          {data ? (
            <Results data={data} />
          ) : (
            <div className="placeholder">
              <p>Загрузите фото и нажмите «Проанализировать», чтобы получить калорийность и БЖУ.</p>
            </div>
          )}
        </section>
      </main>

      <footer className="footer">
        <p>Проект ПрогИнжМ · React + Vite · Express · HuggingFace</p>
      </footer>
    </div>
  );
}
