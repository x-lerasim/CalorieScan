const express = require("express");
const { FOOD_DATABASE } = require("../data/foodDatabase");
const { findFoodData, scaleByPortion } = require("../utils/nutrition");

const router = express.Router();

router.get("/", (req, res) => {
  const list = Object.entries(FOOD_DATABASE).map(([key, value]) => ({ key, ...value }));
  res.json({ count: list.length, items: list });
});

router.get("/:label", (req, res) => {
  const { label } = req.params;
  const portion = Number(req.query.portion) || 200;
  const food = findFoodData(label);
  const scaled = scaleByPortion(food, portion);
  res.json(scaled);
});

module.exports = router;
