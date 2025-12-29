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

# База данных калорий (на 100г продукта) - МАКСИМАЛЬНАЯ БАЗА 100+ ПРОДУКТОВ!
FOOD_DATABASE = {
    # ========== ОСНОВНЫЕ БЛЮДА ==========
    "pizza": {"calories": 266, "protein": 11, "fat": 10, "carbs": 33, "name": "Пицца"},
    "burger": {"calories": 295, "protein": 17, "fat": 14, "carbs": 24, "name": "Бургер"},
    "cheeseburger": {"calories": 303, "protein": 17, "fat": 15, "carbs": 25, "name": "Чизбургер"},
    "hamburger": {"calories": 295, "protein": 17, "fat": 14, "carbs": 24, "name": "Гамбургер"},
    "pasta": {"calories": 131, "protein": 5, "fat": 1, "carbs": 25, "name": "Паста"},
    "spaghetti": {"calories": 158, "protein": 6, "fat": 1, "carbs": 31, "name": "Спагетти"},
    "lasagna": {"calories": 135, "protein": 8, "fat": 5, "carbs": 14, "name": "Лазанья"},
    "sandwich": {"calories": 250, "protein": 12, "fat": 8, "carbs": 32, "name": "Сэндвич"},
    "hot dog": {"calories": 290, "protein": 11, "fat": 17, "carbs": 24, "name": "Хот-дог"},
    "taco": {"calories": 226, "protein": 9, "fat": 13, "carbs": 20, "name": "Тако"},
    "burrito": {"calories": 206, "protein": 10, "fat": 7, "carbs": 26, "name": "Буррито"},
    "quesadilla": {"calories": 234, "protein": 11, "fat": 12, "carbs": 21, "name": "Кесадилья"},
    "wrap": {"calories": 225, "protein": 11, "fat": 9, "carbs": 26, "name": "Ролл"},
    "kebab": {"calories": 195, "protein": 12, "fat": 11, "carbs": 11, "name": "Кебаб"},
    "shawarma": {"calories": 250, "protein": 15, "fat": 14, "carbs": 18, "name": "Шаурма"},

    # ========== МЯСО И ПТИЦА ==========
    "chicken": {"calories": 239, "protein": 27, "fat": 14, "carbs": 0, "name": "Курица"},
    "fried chicken": {"calories": 246, "protein": 19, "fat": 15, "carbs": 9, "name": "Жареная курица"},
    "chicken wings": {"calories": 203, "protein": 30, "fat": 8, "carbs": 0, "name": "Куриные крылышки"},
    "chicken breast": {"calories": 165, "protein": 31, "fat": 3.6, "carbs": 0, "name": "Куриная грудка"},
    "steak": {"calories": 271, "protein": 25, "fat": 19, "carbs": 0, "name": "Стейк"},
    "beef": {"calories": 250, "protein": 26, "fat": 15, "carbs": 0, "name": "Говядина"},
    "pork": {"calories": 242, "protein": 27, "fat": 14, "carbs": 0, "name": "Свинина"},
    "pork chop": {"calories": 231, "protein": 26, "fat": 14, "carbs": 0, "name": "Свиная отбивная"},
    "bacon": {"calories": 541, "protein": 37, "fat": 42, "carbs": 1, "name": "Бекон"},
    "sausage": {"calories": 301, "protein": 12, "fat": 27, "carbs": 2, "name": "Сосиски"},
    "lamb": {"calories": 294, "protein": 25, "fat": 21, "carbs": 0, "name": "Баранина"},
    "duck": {"calories": 337, "protein": 19, "fat": 28, "carbs": 0, "name": "Утка"},
    "turkey": {"calories": 189, "protein": 29, "fat": 7, "carbs": 0, "name": "Индейка"},
    "meatball": {"calories": 197, "protein": 11, "fat": 13, "carbs": 8, "name": "Фрикадельки"},
    "ribs": {"calories": 290, "protein": 23, "fat": 21, "carbs": 0, "name": "Рёбрышки"},

    # ========== РЫБА И МОРЕПРОДУКТЫ ==========
    "fish": {"calories": 206, "protein": 22, "fat": 12, "carbs": 0, "name": "Рыба"},
    "salmon": {"calories": 208, "protein": 20, "fat": 13, "carbs": 0, "name": "Лосось"},
    "tuna": {"calories": 132, "protein": 28, "fat": 1, "carbs": 0, "name": "Тунец"},
    "shrimp": {"calories": 99, "protein": 24, "fat": 0.3, "carbs": 0.2, "name": "Креветки"},
    "lobster": {"calories": 89, "protein": 19, "fat": 0.9, "carbs": 0, "name": "Лобстер"},
    "crab": {"calories": 97, "protein": 19, "fat": 1.5, "carbs": 0, "name": "Краб"},
    "oyster": {"calories": 81, "protein": 9, "fat": 2.3, "carbs": 5, "name": "Устрицы"},
    "calamari": {"calories": 175, "protein": 15, "fat": 7, "carbs": 15, "name": "Кальмары"},
    "cod": {"calories": 82, "protein": 18, "fat": 0.7, "carbs": 0, "name": "Треска"},
    "mackerel": {"calories": 205, "protein": 19, "fat": 14, "carbs": 0, "name": "Скумбрия"},

    # ========== ГАРНИРЫ ==========
    "rice": {"calories": 130, "protein": 2.7, "fat": 0.3, "carbs": 28, "name": "Рис"},
    "fried rice": {"calories": 163, "protein": 4.5, "fat": 5.5, "carbs": 25, "name": "Жареный рис"},
    "potato": {"calories": 77, "protein": 2, "fat": 0.1, "carbs": 17, "name": "Картофель"},
    "fries": {"calories": 312, "protein": 3.4, "fat": 15, "carbs": 41, "name": "Картофель фри"},
    "mashed potato": {"calories": 116, "protein": 2, "fat": 4, "carbs": 18, "name": "Картофельное пюре"},
    "baked potato": {"calories": 93, "protein": 2.5, "fat": 0.1, "carbs": 21, "name": "Запеченный картофель"},
    "sweet potato": {"calories": 86, "protein": 1.6, "fat": 0.1, "carbs": 20, "name": "Батат"},
    "couscous": {"calories": 112, "protein": 3.8, "fat": 0.2, "carbs": 23, "name": "Кускус"},
    "quinoa": {"calories": 120, "protein": 4.4, "fat": 1.9, "carbs": 21, "name": "Киноа"},
    "bulgur": {"calories": 83, "protein": 3, "fat": 0.2, "carbs": 19, "name": "Булгур"},

    # ========== ОВОЩИ И САЛАТЫ ==========
    "salad": {"calories": 15, "protein": 1, "fat": 0.2, "carbs": 3, "name": "Салат"},
    "caesar salad": {"calories": 190, "protein": 9, "fat": 16, "carbs": 5, "name": "Цезарь"},
    "greek salad": {"calories": 106, "protein": 3, "fat": 8, "carbs": 6, "name": "Греческий салат"},
    "vegetables": {"calories": 25, "protein": 1, "fat": 0.2, "carbs": 5, "name": "Овощи"},
    "broccoli": {"calories": 34, "protein": 2.8, "fat": 0.4, "carbs": 7, "name": "Брокколи"},
    "carrot": {"calories": 41, "protein": 0.9, "fat": 0.2, "carbs": 10, "name": "Морковь"},
    "tomato": {"calories": 18, "protein": 0.9, "fat": 0.2, "carbs": 3.9, "name": "Помидор"},
    "cucumber": {"calories": 15, "protein": 0.7, "fat": 0.1, "carbs": 3.6, "name": "Огурец"},
    "pepper": {"calories": 20, "protein": 0.9, "fat": 0.2, "carbs": 4.6, "name": "Перец"},
    "onion": {"calories": 40, "protein": 1.1, "fat": 0.1, "carbs": 9, "name": "Лук"},
    "mushroom": {"calories": 22, "protein": 3.1, "fat": 0.3, "carbs": 3.3, "name": "Грибы"},
    "corn": {"calories": 86, "protein": 3.3, "fat": 1.4, "carbs": 19, "name": "Кукуруза"},
    "peas": {"calories": 81, "protein": 5, "fat": 0.4, "carbs": 14, "name": "Горошек"},
    "beans": {"calories": 127, "protein": 8.7, "fat": 0.5, "carbs": 23, "name": "Фасоль"},
    "spinach": {"calories": 23, "protein": 2.9, "fat": 0.4, "carbs": 3.6, "name": "Шпинат"},

    # ========== СУПЫ ==========
    "soup": {"calories": 45, "protein": 2, "fat": 1, "carbs": 8, "name": "Суп"},
    "chicken soup": {"calories": 56, "protein": 4, "fat": 1.5, "carbs": 7, "name": "Куриный суп"},
    "tomato soup": {"calories": 74, "protein": 2, "fat": 2.5, "carbs": 11, "name": "Томатный суп"},
    "mushroom soup": {"calories": 93, "protein": 3, "fat": 5, "carbs": 9, "name": "Грибной суп"},
    "miso soup": {"calories": 40, "protein": 2, "fat": 1, "carbs": 5, "name": "Мисо суп"},

    # ========== ЗАВТРАКИ ==========
    "egg": {"calories": 155, "protein": 13, "fat": 11, "carbs": 1, "name": "Яйца"},
    "scrambled eggs": {"calories": 149, "protein": 10, "fat": 11, "carbs": 2, "name": "Яичница"},
    "boiled egg": {"calories": 155, "protein": 13, "fat": 11, "carbs": 1, "name": "Вареное яйцо"},
    "omelette": {"calories": 154, "protein": 11, "fat": 12, "carbs": 1, "name": "Омлет"},
    "pancake": {"calories": 227, "protein": 6, "fat": 10, "carbs": 28, "name": "Блины"},
    "waffle": {"calories": 291, "protein": 6, "fat": 10, "carbs": 45, "name": "Вафли"},
    "french toast": {"calories": 166, "protein": 6, "fat": 7, "carbs": 20, "name": "Французские тосты"},
    "toast": {"calories": 265, "protein": 9, "fat": 3, "carbs": 49, "name": "Тост"},
    "cereal": {"calories": 379, "protein": 7, "fat": 4, "carbs": 84, "name": "Хлопья"},
    "oatmeal": {"calories": 68, "protein": 2.4, "fat": 1.4, "carbs": 12, "name": "Овсянка"},
    "granola": {"calories": 471, "protein": 12, "fat": 20, "carbs": 64, "name": "Гранола"},

    # ========== ХЛЕБОБУЛОЧНЫЕ ==========
    "bread": {"calories": 265, "protein": 9, "fat": 3, "carbs": 49, "name": "Хлеб"},
    "white bread": {"calories": 265, "protein": 9, "fat": 3, "carbs": 49, "name": "Белый хлеб"},
    "wheat bread": {"calories": 247, "protein": 13, "fat": 3, "carbs": 41, "name": "Пшеничный хлеб"},
    "croissant": {"calories": 406, "protein": 8, "fat": 21, "carbs": 46, "name": "Круассан"},
    "bagel": {"calories": 257, "protein": 10, "fat": 2, "carbs": 50, "name": "Бейгл"},
    "muffin": {"calories": 377, "protein": 6, "fat": 18, "carbs": 48, "name": "Маффин"},
    "bun": {"calories": 280, "protein": 8, "fat": 4, "carbs": 51, "name": "Булочка"},
    "roll": {"calories": 276, "protein": 9, "fat": 3, "carbs": 52, "name": "Ролл"},
    "pretzel": {"calories": 380, "protein": 9, "fat": 3, "carbs": 79, "name": "Крендель"},

    # ========== ДЕСЕРТЫ И СЛАДКОЕ ==========
    "dessert": {"calories": 350, "protein": 4, "fat": 15, "carbs": 50, "name": "Десерт"},
    "cake": {"calories": 257, "protein": 4, "fat": 10, "carbs": 40, "name": "Торт"},
    "chocolate cake": {"calories": 352, "protein": 5, "fat": 14, "carbs": 51, "name": "Шоколадный торт"},
    "cheesecake": {"calories": 321, "protein": 6, "fat": 23, "carbs": 26, "name": "Чизкейк"},
    "brownie": {"calories": 466, "protein": 6, "fat": 30, "carbs": 50, "name": "Брауни"},
    "ice cream": {"calories": 207, "protein": 3.5, "fat": 11, "carbs": 24, "name": "Мороженое"},
    "cookie": {"calories": 502, "protein": 5, "fat": 23, "carbs": 67, "name": "Печенье"},
    "donut": {"calories": 452, "protein": 5, "fat": 25, "carbs": 51, "name": "Пончик"},
    "chocolate": {"calories": 546, "protein": 5, "fat": 31, "carbs": 61, "name": "Шоколад"},
    "candy": {"calories": 400, "protein": 0, "fat": 9, "carbs": 89, "name": "Конфеты"},
    "pie": {"calories": 237, "protein": 2, "fat": 11, "carbs": 34, "name": "Пирог"},
    "pudding": {"calories": 131, "protein": 3, "fat": 2.8, "carbs": 24, "name": "Пудинг"},
    "tiramisu": {"calories": 240, "protein": 5, "fat": 13, "carbs": 25, "name": "Тирамису"},
    "cupcake": {"calories": 305, "protein": 4, "fat": 13, "carbs": 44, "name": "Капкейк"},

    # ========== ФРУКТЫ ==========
    "fruit": {"calories": 52, "protein": 0.3, "fat": 0.2, "carbs": 14, "name": "Фрукты"},
    "apple": {"calories": 52, "protein": 0.3, "fat": 0.2, "carbs": 14, "name": "Яблоко"},
    "banana": {"calories": 89, "protein": 1.1, "fat": 0.3, "carbs": 23, "name": "Банан"},
    "orange": {"calories": 47, "protein": 0.9, "fat": 0.1, "carbs": 12, "name": "Апельсин"},
    "strawberry": {"calories": 32, "protein": 0.7, "fat": 0.3, "carbs": 7.7, "name": "Клубника"},
    "watermelon": {"calories": 30, "protein": 0.6, "fat": 0.2, "carbs": 8, "name": "Арбуз"},
    "grape": {"calories": 69, "protein": 0.7, "fat": 0.2, "carbs": 18, "name": "Виноград"},
    "pineapple": {"calories": 50, "protein": 0.5, "fat": 0.1, "carbs": 13, "name": "Ананас"},
    "mango": {"calories": 60, "protein": 0.8, "fat": 0.4, "carbs": 15, "name": "Манго"},
    "berry": {"calories": 57, "protein": 0.7, "fat": 0.3, "carbs": 14, "name": "Ягоды"},
    "peach": {"calories": 39, "protein": 0.9, "fat": 0.3, "carbs": 10, "name": "Персик"},
    "pear": {"calories": 57, "protein": 0.4, "fat": 0.1, "carbs": 15, "name": "Груша"},

    # ========== НАПИТКИ И ЖИДКИЕ БЛЮДА ==========
    "smoothie": {"calories": 150, "protein": 3, "fat": 2, "carbs": 30, "name": "Смузи"},
    "juice": {"calories": 45, "protein": 0.5, "fat": 0.1, "carbs": 11, "name": "Сок"},
    "milkshake": {"calories": 223, "protein": 8, "fat": 9, "carbs": 28, "name": "Молочный коктейль"},
    "coffee": {"calories": 2, "protein": 0.3, "fat": 0, "carbs": 0, "name": "Кофе"},
    "latte": {"calories": 103, "protein": 6, "fat": 4, "carbs": 11, "name": "Латте"},
    "cappuccino": {"calories": 74, "protein": 4, "fat": 4, "carbs": 6, "name": "Капучино"},

    # ========== АЗИАТСКАЯ КУХНЯ ==========
    "sushi": {"calories": 143, "protein": 6, "fat": 3.7, "carbs": 21, "name": "Суши"},
    "sashimi": {"calories": 127, "protein": 20, "fat": 5, "carbs": 0, "name": "Сашими"},
    "ramen": {"calories": 188, "protein": 7.9, "fat": 7, "carbs": 27, "name": "Рамен"},
    "udon": {"calories": 105, "protein": 3, "fat": 0.5, "carbs": 22, "name": "Удон"},
    "noodles": {"calories": 138, "protein": 4.5, "fat": 2, "carbs": 25, "name": "Лапша"},
    "pad thai": {"calories": 345, "protein": 9, "fat": 15, "carbs": 44, "name": "Пад Тай"},
    "spring roll": {"calories": 120, "protein": 3, "fat": 4, "carbs": 18, "name": "Спринг-ролл"},
    "dumpling": {"calories": 175, "protein": 7, "fat": 6, "carbs": 23, "name": "Пельмени"},
    "tempura": {"calories": 130, "protein": 3, "fat": 5, "carbs": 18, "name": "Темпура"},
    "teriyaki": {"calories": 170, "protein": 18, "fat": 6, "carbs": 12, "name": "Терияки"},

    # ========== РАЗНОЕ ==========
    "cheese": {"calories": 402, "protein": 25, "fat": 33, "carbs": 1.3, "name": "Сыр"},
    "mozzarella": {"calories": 280, "protein": 28, "fat": 17, "carbs": 3, "name": "Моцарелла"},
    "cheddar": {"calories": 403, "protein": 25, "fat": 33, "carbs": 1.3, "name": "Чеддер"},
    "yogurt": {"calories": 59, "protein": 10, "fat": 0.4, "carbs": 3.6, "name": "Йогурт"},
    "milk": {"calories": 42, "protein": 3.4, "fat": 1, "carbs": 5, "name": "Молоко"},
    "butter": {"calories": 717, "protein": 0.9, "fat": 81, "carbs": 0.1, "name": "Масло"},
    "nuts": {"calories": 607, "protein": 20, "fat": 54, "carbs": 21, "name": "Орехи"},
    "peanut": {"calories": 567, "protein": 26, "fat": 49, "carbs": 16, "name": "Арахис"},
    "almond": {"calories": 579, "protein": 21, "fat": 50, "carbs": 22, "name": "Миндаль"},
    "avocado": {"calories": 160, "protein": 2, "fat": 15, "carbs": 9, "name": "Авокадо"},
    "hummus": {"calories": 166, "protein": 8, "fat": 10, "carbs": 14, "name": "Хумус"},
    "guacamole": {"calories": 161, "protein": 2, "fat": 15, "carbs": 9, "name": "Гуакамоле"},
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
    food_label_lower = food_label.lower()

    # Сначала ищем точное совпадение
    if food_label_lower in FOOD_DATABASE:
        food_data = FOOD_DATABASE[food_label_lower].copy()
    else:
        # Ищем частичное совпадение (ключевые слова)
        food_data = None
        for key in FOOD_DATABASE.keys():
            if key in food_label_lower or food_label_lower in key:
                food_data = FOOD_DATABASE[key].copy()
                break

        # Если не найдено - используем название модели с средними значениями
        if food_data is None:
            # Красиво форматируем название
            formatted_name = food_label.replace('_', ' ').title()
            food_data = {
                "name": f"{formatted_name} (приблизительно)",
                "calories": 200,
                "protein": 10,
                "fat": 8,
                "carbs": 25
            }

    # Пересчитываем на указанную порцию
    multiplier = portion_size / 100
    food_data["calories"] = round(food_data["calories"] * multiplier)
    food_data["protein"] = round(food_data["protein"] * multiplier, 1)
    food_data["fat"] = round(food_data["fat"] * multiplier, 1)
    food_data["carbs"] = round(food_data["carbs"] * multiplier, 1)

    return food_data


# Заголовок приложения
st.title("🍕 CalorieScan - AI Счетчик Калорий")
st.markdown("### Загрузите фото еды и узнайте калорийность!")

# Боковая панель с информацией
with st.sidebar:
    st.header("ℹ️ О приложении")
    st.write(f"""
    **CalorieScan** использует AI для:
    - 🔍 Распознавания еды на фото
    - 📊 Подсчета калорий и БЖУ
    - 💡 Рекомендаций по питанию

    **Модель:** HuggingFace Food Classification
    **База продуктов:** {len(FOOD_DATABASE)} категорий еды! 🎉
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

                    # Показываем оригинальное название модели если оно отличается
                    formatted_model_name = food_label.replace('_', ' ').title()
                    if formatted_model_name.lower() not in nutrition['name'].lower():
                        st.info(f"🔍 Модель распознала как: *{formatted_model_name}*")

                    st.info(f"🎯 Уверенность модели: **{confidence * 100:.1f}%**")

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
