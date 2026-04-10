import { render, screen } from "@testing-library/react";
import { describe, test, expect } from "vitest";
import MacroBar from "../components/MacroBar.jsx";

describe("MacroBar", () => {
  test("renders all macronutrient labels and values", () => {
    render(<MacroBar protein={20} fat={10} carbs={30} />);
    expect(screen.getByText(/Белки/)).toBeInTheDocument();
    expect(screen.getByText(/Жиры/)).toBeInTheDocument();
    expect(screen.getByText(/Углеводы/)).toBeInTheDocument();
    expect(screen.getByText(/20г/)).toBeInTheDocument();
    expect(screen.getByText(/10г/)).toBeInTheDocument();
    expect(screen.getByText(/30г/)).toBeInTheDocument();
  });

  test("handles zero values without crashing", () => {
    render(<MacroBar protein={0} fat={0} carbs={0} />);
    expect(screen.getByLabelText(/Распределение БЖУ/)).toBeInTheDocument();
  });
});
