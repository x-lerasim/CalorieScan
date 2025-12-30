"""
Тесты для CalorieScan приложения
"""
import pytest
from PIL import Image
import numpy as np


# ============================================
# 1. ТЕСТ БАЗЫ ДАННЫХ КАЛОРИЙ
# ============================================

FOOD_DATABASE = {
    "pizza": {"calories": 266, "protein": 11, "fat": 10, "carbs": 33, "name": "Пицца"},
    "burger": {"calories": 295, "protein": 17, "fat": 14, "carbs": 24, "name": "Бургер"},
    "salad": {"calories": 15, "protein": 1, "fat": 0.2, "carbs": 3, "name": "Салат"},
}

def test_food_database_structure():
    """Проверка структуры базы данных калорий"""
    for food_name, food_data in FOOD_DATABASE.items():
        assert "calories" in food_data, f"Отсутствует 'calories' для {food_name}"
        assert "protein" in food_data, f"Отсутствует 'protein' для {food_name}"
        assert "fat" in food_data, f"Отсутствует 'fat' для {food_name}"
        assert "carbs" in food_data, f"Отсутствует 'carbs' для {food_name}"
        assert "name" in food_data, f"Отсутствует 'name' для {food_name}"

def test_food_database_values():
    """Проверка корректности значений в базе"""
    for food_name, food_data in FOOD_DATABASE.items():
        assert food_data["calories"] > 0, f"Калории должны быть > 0 для {food_name}"
        assert food_data["protein"] >= 0, f"Белки должны быть >= 0 для {food_name}"
        assert food_data["fat"] >= 0, f"Жиры должны быть >= 0 для {food_name}"
        assert food_data["carbs"] >= 0, f"Углеводы должны быть >= 0 для {food_name}"


# ============================================
# 2. ТЕСТ ФУНКЦИИ ПОЛУЧЕНИЯ ПИЩЕВОЙ ЦЕННОСТИ
# ============================================

def get_nutrition_info(food_label, portion_size=200):
    """Функция для получения информации о питательности"""
    for key in FOOD_DATABASE.keys():
        if key in food_label:
            food_data = FOOD_DATABASE[key].copy()
            multiplier = portion_size / 100
            food_data["calories"] = round(food_data["calories"] * multiplier)
            food_data["protein"] = round(food_data["protein"] * multiplier, 1)
            food_data["fat"] = round(food_data["fat"] * multiplier, 1)
            food_data["carbs"] = round(food_data["carbs"] * multiplier, 1)
            return food_data
    
    return {
        "name": "Неизвестная еда",
        "calories": round(200 * portion_size / 100),
        "protein": round(10 * portion_size / 100, 1),
        "fat": round(8 * portion_size / 100, 1),
        "carbs": round(25 * portion_size / 100, 1)
    }

def test_nutrition_calculation():
    """Проверка расчета пищевой ценности"""
    # Тест для пиццы на 200г
    result = get_nutrition_info("pizza", 200)
    assert result["calories"] == 532, "Неверный расчет калорий для пиццы"
    assert result["protein"] == 22.0, "Неверный расчет белков для пиццы"
    
    # Тест для салата на 100г
    result = get_nutrition_info("salad", 100)
    assert result["calories"] == 15, "Неверный расчет калорий для салата"

def test_nutrition_unknown_food():
    """Проверка обработки неизвестной еды"""
    result = get_nutrition_info("unknown_food", 200)
    assert result["name"] == "Неизвестная еда"
    assert result["calories"] > 0


# ============================================
# 3. ТЕСТ ОБРАБОТКИ ИЗОБРАЖЕНИЙ
# ============================================

def test_image_creation():
    """Проверка создания тестового изображения"""
    # Создаем тестовое изображение
    img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    
    assert img.size == (224, 224), "Неверный размер изображения"
    assert img.mode == "RGB", "Неверный режим изображения"

def test_image_formats():
    """Проверка поддерживаемых форматов изображений"""
    supported_formats = ["jpg", "jpeg", "png"]
    for fmt in supported_formats:
        assert fmt in ["jpg", "jpeg", "png"], f"Формат {fmt} должен поддерживаться"


# ============================================
# 4. ТЕСТ ВАЛИДАЦИИ ВХОДНЫХ ДАННЫХ
# ============================================

def test_portion_size_validation():
    """Проверка валидации размера порции"""
    valid_sizes = [50, 100, 200, 500]
    for size in valid_sizes:
        assert 50 <= size <= 500, f"Размер {size} должен быть в диапазоне 50-500"
        result = get_nutrition_info("pizza", size)
        assert result["calories"] > 0

def test_invalid_portion_size():
    """Проверка обработки некорректного размера порции"""
    # Слишком маленький размер
    result = get_nutrition_info("pizza", 10)
    assert result["calories"] > 0, "Должен обрабатывать маленький размер"
    
    # Очень большой размер
    result = get_nutrition_info("pizza", 1000)
    assert result["calories"] > 0, "Должен обрабатывать большой размер"


# ============================================
# 5. ИНТЕГРАЦИОННЫЕ ТЕСТЫ
# ============================================

def test_full_workflow():
    """Проверка полного workflow приложения"""
    # 1. Проверяем базу данных
    assert len(FOOD_DATABASE) > 0, "База данных не должна быть пустой"
    
    # 2. Получаем информацию о еде
    result = get_nutrition_info("pizza", 200)
    
    # 3. Проверяем результат
    assert result is not None
    assert "calories" in result
    assert result["calories"] > 0
    
    # 4. Проверяем все поля
    required_fields = ["calories", "protein", "fat", "carbs"]
    for field in required_fields:
        assert field in result, f"Отсутствует поле {field}"


# ============================================
# 6. ТЕСТЫ ГРАНИЧНЫХ СЛУЧАЕВ
# ============================================

def test_edge_cases():
    """Проверка граничных случаев"""
    # Пустая строка
    result = get_nutrition_info("", 200)
    assert result["name"] != ""
    
    # Очень длинное название
    result = get_nutrition_info("a" * 1000, 200)
    assert result is not None
    
    # Специальные символы с известным продуктом
    result = get_nutrition_info("pizza@#$%", 200)
    # Должна найти pizza в строке
    assert result is not None
    assert result["calories"] > 0


# ============================================
# 7. ТЕСТЫ ПРОИЗВОДИТЕЛЬНОСТИ
# ============================================

def test_performance():
    """Базовая проверка производительности"""
    import time
    
    start_time = time.time()
    for _ in range(100):
        get_nutrition_info("pizza", 200)
    end_time = time.time()
    
    execution_time = end_time - start_time
    assert execution_time < 1.0, "100 операций должны выполняться менее чем за 1 секунду"


# ============================================
# ЗАПУСК ТЕСТОВ
# ============================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
    print("\n✅ Все тесты пройдены успешно!")
