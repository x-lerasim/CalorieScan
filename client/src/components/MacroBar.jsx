import React from "react";

const COLORS = {
  protein: "#4f9de8",
  fat: "#f59e0b",
  carbs: "#22c55e"
};

export default function MacroBar({ protein, fat, carbs }) {
  const total = Math.max(protein + fat + carbs, 0.0001);
  const items = [
    { key: "protein", label: "Белки", value: protein },
    { key: "fat", label: "Жиры", value: fat },
    { key: "carbs", label: "Углеводы", value: carbs }
  ];

  return (
    <div className="macro-bar" aria-label="Распределение БЖУ">
      <div className="macro-track">
        {items.map((item) => (
          <div
            key={item.key}
            className="macro-segment"
            style={{
              width: `${(item.value / total) * 100}%`,
              backgroundColor: COLORS[item.key]
            }}
            title={`${item.label}: ${item.value}г`}
          />
        ))}
      </div>
      <ul className="macro-legend">
        {items.map((item) => (
          <li key={item.key}>
            <span className="dot" style={{ backgroundColor: COLORS[item.key] }} />
            {item.label}: <strong>{item.value}г</strong>
          </li>
        ))}
      </ul>
    </div>
  );
}
