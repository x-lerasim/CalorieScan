const express = require("express");
const multer = require("multer");
const { classifyImage } = require("../services/huggingface");
const { findFoodData, scaleByPortion, buildRecommendation } = require("../utils/nutrition");

const router = express.Router();

const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    if (!file.mimetype.startsWith("image/")) {
      return cb(new Error("Only image files are allowed"));
    }
    cb(null, true);
  }
});

router.post("/", upload.single("image"), async (req, res, next) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "Image file is required (field name: image)" });
    }
    const rawPortion = req.body.portion;
    const portionRequested =
      rawPortion === undefined || rawPortion === "" || rawPortion === null
        ? undefined
        : Number(rawPortion);
    const { label, confidence } = await classifyImage(req.file.buffer);
    const food = findFoodData(label);
    const nutrition = scaleByPortion(food, portionRequested);
    const recommendation = buildRecommendation(nutrition.calories);
    res.json({
      label,
      confidence,
      nutrition,
      recommendation
    });
  } catch (err) {
    next(err);
  }
});

module.exports = router;
