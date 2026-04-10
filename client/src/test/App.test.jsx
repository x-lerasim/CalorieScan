import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, test, expect, vi, beforeEach } from "vitest";

vi.mock("../api.js", () => ({
  analyzeImage: vi.fn(),
  fetchHealth: vi.fn()
}));

import App from "../App.jsx";
import { analyzeImage } from "../api.js";

describe("App", () => {
  beforeEach(() => {
    analyzeImage.mockReset();
  });

  test("renders header and default placeholder", () => {
    render(<App />);
    expect(screen.getByText(/CalorieScan/i)).toBeInTheDocument();
    expect(screen.getByText(/AI-счётчик калорий/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Проанализировать/ })).toBeDisabled();
  });

  test("analyze button is disabled without a file", () => {
    render(<App />);
    const analyzeBtn = screen.getByRole("button", { name: /Проанализировать/ });
    expect(analyzeBtn).toBeDisabled();
    expect(analyzeImage).not.toHaveBeenCalled();
  });

  test("analyzes file and renders results", async () => {
    analyzeImage.mockResolvedValue({
      label: "pizza",
      confidence: 0.95,
      nutrition: {
        name: "Пицца",
        matched: true,
        calories: 532,
        protein: 22,
        fat: 20,
        carbs: 66,
        portionSize: 200
      },
      recommendation: { level: "warning", text: "Высококалорийное блюдо." }
    });
    const user = userEvent.setup();
    render(<App />);

    const file = new File(["fake"], "pizza.jpg", { type: "image/jpeg" });
    const input = screen.getByTestId("file-input");
    await user.upload(input, file);

    const analyzeBtn = screen.getByRole("button", { name: /Проанализировать/ });
    await waitFor(() => expect(analyzeBtn).not.toBeDisabled());
    await user.click(analyzeBtn);

    await waitFor(() => {
      expect(analyzeImage).toHaveBeenCalledTimes(1);
    });
    await waitFor(() => {
      expect(screen.getByTestId("results")).toBeInTheDocument();
    });
    expect(screen.getByText("Пицца")).toBeInTheDocument();
    expect(screen.getByText("532")).toBeInTheDocument();
  });

  test("shows error message when API rejects", async () => {
    analyzeImage.mockRejectedValue(new Error("Сервер недоступен"));
    const user = userEvent.setup();
    render(<App />);

    const file = new File(["fake"], "pizza.jpg", { type: "image/jpeg" });
    const input = screen.getByTestId("file-input");
    await user.upload(input, file);

    const analyzeBtn = screen.getByRole("button", { name: /Проанализировать/ });
    await waitFor(() => expect(analyzeBtn).not.toBeDisabled());
    await user.click(analyzeBtn);

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent(/Сервер недоступен/);
    });
  });
});
