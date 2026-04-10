const { FOOD_DATABASE } = require("../data/foodDatabase");

function findFoodData(label) {
  if (!label) return null;
  const key = label.toLowerCase().trim();
  if (FOOD_DATABASE[key]) {
    return { ...FOOD_DATABASE[key], matched: true };
  }
  for (const dbKey of Object.keys(FOOD_DATABASE)) {
    if (key.includes(dbKey) || dbKey.includes(key)) {
      return { ...FOOD_DATABASE[dbKey], matched: true };
    }
  }
  const formatted = label.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
  return {
    name: `${formatted} (приблизительно)`,
    calories: 200,
    protein: 10,
    fat: 8,
    carbs: 25,
    matched: false
  };
}

function scaleByPortion(food, portionSize) {
  const portion = Number(portionSize) || 200;
  const multiplier = portion / 100;
  return {
    name: food.name,
    matched: food.matched,
    calories: Math.round(food.calories * multiplier),
    protein: Math.round(food.protein * multiplier * 10) / 10,
    fat: Math.round(food.fat * multiplier * 10) / 10,
    carbs: Math.round(food.carbs * multiplier * 10) / 10,
    portionSize: portion
  };
}

function buildRecommendation(calories) {
  if (calories > 400) {
    return {
      level: "warning",
      text: "Высококалорийное блюдо. Подходит для основного приема пищи."
    };
  }
  if (calories < 100) {
    return { level: "info", text: "Легкое блюдо. Отлично для перекуса!" };
  }
  return { level: "success", text: "Сбалансированное блюдо." };
}

module.exports = { findFoodData, scaleByPortion, buildRecommendation };
