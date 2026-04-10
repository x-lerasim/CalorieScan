const express = require("express");
const cors = require("cors");
const morgan = require("morgan");

const healthRouter = require("./routes/health");
const foodsRouter = require("./routes/foods");
const analyzeRouter = require("./routes/analyze");

function createApp() {
  const app = express();

  const allowedOrigins = (process.env.CORS_ORIGIN || "*")
    .split(",")
    .map((o) => o.trim())
    .filter(Boolean);

  app.use(
    cors({
      origin: allowedOrigins.includes("*") ? true : allowedOrigins,
      credentials: true
    })
  );
  app.use(express.json({ limit: "2mb" }));
  if (process.env.NODE_ENV !== "test") {
    app.use(morgan("tiny"));
  }

  app.use("/api/health", healthRouter);
  app.use("/api/foods", foodsRouter);
  app.use("/api/analyze", analyzeRouter);

  app.get("/", (req, res) => {
    res.json({
      service: "CalorieScan API",
      endpoints: ["/api/health", "/api/foods", "/api/foods/:label", "/api/analyze"]
    });
  });

  app.use((req, res) => {
    res.status(404).json({ error: "Not found", path: req.originalUrl });
  });

  app.use((err, req, res, _next) => {
    const status = err.status || 500;
    res.status(status).json({
      error: err.message || "Internal server error"
    });
  });

  return app;
}

module.exports = { createApp };
