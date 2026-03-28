#  CalorieScan - AI Счетчик Калорий

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)

**CalorieScan** - веб-приложение для подсчета калорий и анализа пищевой ценности еды по фотографии с использованием искусственного интеллекта.

##  Описание проекта

Проект разработан в рамках курса "Проектный практикум" (ПрогИнжМ). Приложение использует предобученную модель компьютерного зрения для распознавания еды на фотографиях и автоматического подсчета калорий, белков, жиров и углеводов.

### Ключевые возможности:
-  Распознавание еды на фотографии
-  Автоматический подсчет калорий и БЖУ
-  Визуализация пищевой ценности
-  Настройка размера порции
-  Рекомендации по питанию

##  Демо

** Живое демо:** [CalorieScan на Streamlit Cloud]([https://caloriescan123.streamlit.app/])(https://caloriescan123.streamlit.app/)

** Google Colab:** [Демонстрация модели]([https://colab.research.google.com/drive/1EuQG9Niok1pQC45_jw1ly3e9BKXXn80n?usp=sharing])(https://colab.research.google.com/drive/1EuQG9Niok1pQC45_jw1ly3e9BKXXn80n?usp=sharing)

##  Технологии

- **Frontend:** Streamlit
- **ML Framework:** PyTorch, HuggingFace Transformers
- **Модель:** [nateraw/food](https://huggingface.co/nateraw/food)
- **CI/CD:** GitHub Actions
- **Деплой:** Streamlit Cloud

##  Установка и запуск

### Требования
- Python 3.8+
- pip

### Локальная установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/CalorieScan.git
cd CalorieScan
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите приложение:
```bash
streamlit run app.py
```

4. Откройте в браузере: `http://localhost:8501`

##  Структура проекта

```
CalorieScan/
├── app.py                          # Основное Streamlit приложение
├── requirements.txt                # Зависимости проекта
├── tests/
│   └── test_app.py                # Тесты
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI/CD
├── README.md                       # Документация
└── .gitignore                     # Игнорируемые файлы
```

##  Тестирование

Запуск тестов:
```bash
pytest tests/
```

##  Модель

Используется предобученная модель **nateraw/food** из HuggingFace:
- **Архитектура:** Vision Transformer (ViT)
- **Датасет:** Food-101
- **Классы:** 101 категория еды
- **Точность:** ~85% на тестовой выборке

##  База данных калорий

Приложение использует встроенную базу данных с информацией о пищевой ценности:
- Калории 
- Белки, жиры, углеводы
- 100+ категорий еды

##  CI/CD

Проект использует GitHub Actions для автоматического тестирования:
- Автоматический запуск тестов при push
- Проверка кода на ошибки
- Автоматический деплой на Streamlit Cloud

