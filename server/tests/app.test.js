const request = require("supertest");

jest.mock("../src/services/huggingface", () => ({
  classifyImage: jest.fn()
}));

const { classifyImage } = require("../src/services/huggingface");
const { createApp } = require("../src/app");

const app = createApp();

describe("GET /api/health", () => {
  test("returns ok status", async () => {
    const res = await request(app).get("/api/health");
    expect(res.status).toBe(200);
    expect(res.body.status).toBe("ok");
    expect(res.body.service).toBe("caloriescan-api");
  });
});

describe("GET /api/foods", () => {
  test("returns the full food list", async () => {
    const res = await request(app).get("/api/foods");
    expect(res.status).toBe(200);
    expect(res.body.count).toBeGreaterThan(100);
    expect(Array.isArray(res.body.items)).toBe(true);
    expect(res.body.items[0]).toHaveProperty("calories");
  });
});

describe("GET /api/foods/:label", () => {
  test("returns scaled data for known label", async () => {
    const res = await request(app).get("/api/foods/pizza?portion=100");
    expect(res.status).toBe(200);
    expect(res.body.name).toBe("Пицца");
    expect(res.body.calories).toBe(266);
    expect(res.body.matched).toBe(true);
  });

  test("scales by portion parameter", async () => {
    const res = await request(app).get("/api/foods/pizza?portion=200");
    expect(res.body.calories).toBe(532);
  });
});

describe("POST /api/analyze", () => {
  beforeEach(() => {
    classifyImage.mockReset();
  });

  test("returns nutrition for classified image", async () => {
    classifyImage.mockResolvedValue({ label: "pizza", confidence: 0.95 });
    const res = await request(app)
      .post("/api/analyze")
      .attach("image", Buffer.from("fake-image-data"), "food.jpg")
      .field("portion", "200");
    expect(res.status).toBe(200);
    expect(res.body.label).toBe("pizza");
    expect(res.body.confidence).toBeCloseTo(0.95);
    expect(res.body.nutrition.name).toBe("Пицца");
    expect(res.body.nutrition.calories).toBe(532);
    expect(res.body.recommendation.level).toBe("warning");
  });

  test("returns 400 when image is missing", async () => {
    const res = await request(app).post("/api/analyze").field("portion", "200");
    expect(res.status).toBe(400);
    expect(res.body.error).toMatch(/image/i);
  });

  test("propagates service errors", async () => {
    const err = new Error("HF down");
    err.status = 502;
    classifyImage.mockRejectedValue(err);
    const res = await request(app)
      .post("/api/analyze")
      .attach("image", Buffer.from("fake"), "food.jpg");
    expect(res.status).toBe(502);
    expect(res.body.error).toBe("HF down");
  });

  test("rejects non-image uploads", async () => {
    const res = await request(app)
      .post("/api/analyze")
      .attach("image", Buffer.from("text"), { filename: "file.txt", contentType: "text/plain" });
    expect(res.status).toBe(500);
  });
});

describe("unknown routes", () => {
  test("returns 404", async () => {
    const res = await request(app).get("/api/unknown");
    expect(res.status).toBe(404);
    expect(res.body.error).toBe("Not found");
  });
});
