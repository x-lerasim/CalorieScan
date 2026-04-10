import { render, screen } from "@testing-library/react";
import { describe, test, expect } from "vitest";
import Results from "../components/Results.jsx";

const sampleData = {
  label: "pizza",
  confidence: 0.9234,
  nutrition: {
    name: "Пицца",
    matched: true,
    calories: 532,
    protein: 22,
    fat: 20,
    carbs: 66,
    portionSize: 200
  },
  recommendation: {
    level: "warning",
    text: "Высококалорийное блюдо. Подходит для основного приема пищи."
  }
};

describe("Results", () => {
  test("returns null when no data is provided", () => {
    const { container } = render(<Results data={null} />);
    expect(container.firstChild).toBeNull();
  });

  test("renders detected food name, calories, macros, and recommendation", () => {
    render(<Results data={sampleData} />);
    expect(screen.getByText("Пицца")).toBeInTheDocument();
    expect(screen.getByText("532")).toBeInTheDocument();
    expect(screen.getByText(/92.3%/)).toBeInTheDocument();
    expect(screen.getByText(/Высококалорийное блюдо/)).toBeInTheDocument();
    expect(screen.getByText(/22 г/)).toBeInTheDocument();
    expect(screen.getByText(/20 г/)).toBeInTheDocument();
    expect(screen.getByText(/66 г/)).toBeInTheDocument();
  });
});
