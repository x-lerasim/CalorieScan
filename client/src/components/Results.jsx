import React from "react";
import MacroBar from "./MacroBar.jsx";

export default function Results({ data }) {
  if (!data) return null;
  const { label, confidence, nutrition, recommendation } = data;

  return (
    <div className="results-card" data-testid="results">
      <h2>Результаты анализа</h2>
      <div className="detection">
        <span className="detection-dot" />
        <div>
          <p className="detection-name">{nutrition.name}</p>
          <p className="detection-meta">
            Модель: <em>{label}</em> · Уверенность{" "}
            <strong>{(confidence * 100).toFixed(1)}%</strong>
          </p>
          <p className="detection-meta">
            Порция:{" "}
            <strong>
              {nutrition.portionSize} г
              {nutrition.portionAuto ? " (определено автоматически)" : ""}
            </strong>
          </p>
        </div>
      </div>

      <div className="calories">
        <span className="calories-value">{nutrition.calories}</span>
        <span className="calories-unit">ккал</span>
      </div>

      <div className="metrics">
        <div className="metric">
          <span className="metric-label">Белки</span>
          <span className="metric-value">{nutrition.protein} г</span>
        </div>
        <div className="metric">
          <span className="metric-label">Жиры</span>
          <span className="metric-value">{nutrition.fat} г</span>
        </div>
        <div className="metric">
          <span className="metric-label">Углеводы</span>
          <span className="metric-value">{nutrition.carbs} г</span>
        </div>
      </div>

      <h3>Состав БЖУ</h3>
      <MacroBar
        protein={nutrition.protein}
        fat={nutrition.fat}
        carbs={nutrition.carbs}
      />

      <div className={`recommendation recommendation-${recommendation.level}`}>
        {recommendation.text}
      </div>
    </div>
  );
}
