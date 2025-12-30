import streamlit as st
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
import json

# Конфигурация страницы
st.set_page_config(
    page_title="CalorieScan - AI Счетчик Калорий",
    page_icon="🍕",
    layout="wide"
)

# База данных калорий (на 100г продукта)
FOOD_DATABASE = {
    "pizza": {"calories": 266, "protein": 11, "fat": 10, "carbs": 33, "name": "Пицца"},
    "burger": {"calories": 295, "protein": 17, "fat": 14, "carbs": 24, "name": "Бургер"},
    "salad": {"calories": 15, "protein": 1, "fat": 0.2, "carbs": 3, "name": "Салат"},
    "pasta": {"calories": 131, "protein": 5, "fat": 1, "carbs": 25, "name": "Паста"},
    "chicken": {"calories": 239, "protein": 27, "fat": 14, "carbs": 0, "name": "Курица"},
    "steak": {"calories": 271, "protein": 25, "fat": 19, "carbs": 0, "name": "Стейк"},
    "rice": {"calories": 130, "protein": 2.7, "fat": 0.3, "carbs": 28, "name": "Рис"},
    "sandwich": {"calories": 250, "protein": 12, "fat": 8, "carbs": 32, "name": "Сэндвич"},
    "soup": {"calories": 45, "protein": 2, "fat": 1, "carbs": 8, "name": "Суп"},
    "fruit": {"calories": 52, "protein": 0.3, "fat": 0.2, "carbs": 14, "name": "Фрукты"},
    "vegetables": {"calories": 25, "protein": 1, "fat": 0.2, "carbs": 5, "name": "Овощи"},
    "bread": {"calories": 265, "protein": 9, "fat": 3, "carbs": 49, "name": "Хлеб"},
    "fish": {"calories": 206, "protein": 22, "fat": 12, "carbs": 0, "name": "Рыба"},
    "egg": {"calories": 155, "protein": 13, "fat": 11, "carbs": 1, "name": "Яйца"},
    "dessert": {"calories": 350, "protein": 4, "fat": 15, "carbs": 50, "name": "Десерт"},
}

# Кэширование модели
@st.cache_resource
def load_model():
    """Загрузка модели классификации еды"""
    model_name = "nateraw/food"
    try:
        processor = AutoImageProcessor.from_pretrained(model_name)
        model = AutoModelForImageClassification.from_pretrained(model_name)
        return processor, model
    except Exception as e:
        st.error(f"Ошибка загрузки модели: {e}")
        return None, None

def classify_food(image, processor, model):
    """Классификация изображения еды"""
    try:
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = logits.argmax(-1).item()
        confidence = torch.nn.functional.softmax(logits, dim=-1)[0][predicted_class].item()
        
        # Получаем название класса
        label = model.config.id2label[predicted_class].lower()
        
        return label, confidence
    except Exception as e:
        st.error(f"Ошибка классификации: {e}")
        return None, 0

def get_nutrition_info(food_label, portion_size=200):
    """Получение информации о калориях и БЖУ"""
    # Простой поиск по ключевым словам
    for key in FOOD_DATABASE.keys():
        if key in food_label:
            food_data = FOOD_DATABASE[key].copy()
            # Пересчитываем на указанную порцию
            multiplier = portion_size / 100
            food_data["calories"] = round(food_data["calories"] * multiplier)
            food_data["protein"] = round(food_data["protein"] * multiplier, 1)
            food_data["fat"] = round(food_data["fat"] * multiplier, 1)
            food_data["carbs"] = round(food_data["carbs"] * multiplier, 1)
            return food_data
    
    # Если не найдено - возвращаем средние значения
    return {
        "name": "Неизвестная еда",
        "calories": round(200 * portion_size / 100),
        "protein": round(10 * portion_size / 100, 1),
        "fat": round(8 * portion_size / 100, 1),
        "carbs": round(25 * portion_size / 100, 1)
    }

# Заголовок приложения
st.title("🍕 CalorieScan - AI Счетчик Калорий")
st.markdown("### Загрузите фото еды и узнайте калорийность!")

# Боковая панель с информацией
with st.sidebar:
    st.header("ℹ️ О приложении")
    st.write("""
    **CalorieScan** использует AI для:
    - 🔍 Распознавания еды на фото
    - 📊 Подсчета калорий и БЖУ
    - 💡 Рекомендаций по питанию
    
    **Модель:** HuggingFace Food Classification
    """)
    
    st.header("⚙️ Настройки")
    portion_size = st.slider("Размер порции (г)", 50, 500, 200, 50)

# Основной интерфейс
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 Загрузите фото")
    uploaded_file = st.file_uploader("Выберите изображение", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Загруженное фото", use_container_width=True)

with col2:
    st.subheader("📊 Результаты анализа")
    
    if uploaded_file:
        with st.spinner("🤖 Анализирую фото..."):
            # Загружаем модель
            processor, model = load_model()
            
            if processor and model:
                # Классифицируем
                food_label, confidence = classify_food(image, processor, model)
                
                if food_label:
                    # Получаем информацию о питательности
                    nutrition = get_nutrition_info(food_label, portion_size)
                    
                    st.success(f"✅ Обнаружено: **{nutrition['name']}**")
                    st.info(f"🎯 Уверенность модели: **{confidence*100:.1f}%**")
                    
                    # Отображаем калории
                    st.metric("🔥 Калории", f"{nutrition['calories']} ккал")
                    
                    # БЖУ в трех колонках
                    col_p, col_f, col_c = st.columns(3)
                    with col_p:
                        st.metric("🥩 Белки", f"{nutrition['protein']}г")
                    with col_f:
                        st.metric("🧈 Жиры", f"{nutrition['fat']}г")
                    with col_c:
                        st.metric("🍞 Углеводы", f"{nutrition['carbs']}г")
                    
                    # График БЖУ
                    st.subheader("📈 Состав БЖУ")
                    chart_data = {
                        "Белки": nutrition['protein'],
                        "Жиры": nutrition['fat'],
                        "Углеводы": nutrition['carbs']
                    }
                    st.bar_chart(chart_data)
                    
                    # Рекомендации
                    st.subheader("💡 Рекомендации")
                    if nutrition['calories'] > 400:
                        st.warning("⚠️ Высококалорийное блюдо. Подходит для основного приема пищи.")
                    elif nutrition['calories'] < 100:
                        st.info("✅ Легкое блюдо. Отлично для перекуса!")
                    else:
                        st.success("✅ Сбалансированное блюдо.")
    else:
        st.info("👆 Загрузите фото еды для анализа")

# Футер
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🎓 Проект "ПрогИнжМ" | Сделано с ❤️ используя Streamlit и HuggingFace</p>
</div>
""", unsafe_allow_html=True)