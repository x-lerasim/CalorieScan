# CalorieScan — Full-Stack AI счётчик калорий

Полноценное веб-приложение: загружаете фото еды — получаете название блюда, калории и БЖУ.
Фронтенд на **React + Vite**, бэкенд на **Node.js + Express**, ML — через **HuggingFace Inference API**
(модель `nateraw/food`). Тесты, CI/CD и бесплатный хостинг — всё уже настроено.

## Структура репозитория

```
CalorieScan/
├── client/                 # React + Vite фронтенд
│   ├── src/
│   │   ├── components/     # ImageUpload, Results, MacroBar
│   │   ├── test/           # Vitest тесты
│   │   ├── App.jsx
│   │   ├── api.js
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── vercel.json
├── server/                 # Express REST API
│   ├── src/
│   │   ├── routes/         # /api/health, /api/foods, /api/analyze
│   │   ├── services/       # HuggingFace клиент
│   │   ├── data/           # База продуктов (≈140 позиций)
│   │   ├── utils/          # findFoodData, scaleByPortion, рекомендации
│   │   ├── app.js          # Express приложение
│   │   └── index.js        # entry point
│   ├── tests/              # Jest + Supertest тесты
│   └── package.json
├── .github/workflows/ci.yml  # тесты + авто-деплой
├── render.yaml               # backend infra as code (Render)
└── README.md
```

## Почему именно эти хостинги

- **Vercel (фронт)** — оптимален для Vite/React. Преимущества: бесплатный SSL, мгновенные
  preview-деплои на каждый PR, edge CDN из коробки, нативная поддержка Vite. Плюс готовый CLI
  (`vercel deploy --prebuilt`) для интеграции из GitHub Actions.
- **Render (бэк)** — в отличие от Railway, где бесплатный уровень ограничен $5 кредитами,
  у Render есть настоящий бессрочный Free Web Service для Node.js. Поддерживает Deploy Hooks
  (простой `curl POST` из CI запускает деплой) и IaC через `render.yaml`. Идеально для Express.

## Технологический стек

| Слой        | Технологии                                         |
| ----------- | -------------------------------------------------- |
| Frontend    | React 18, Vite 5, Vitest, Testing Library           |
| Backend     | Node.js 20, Express 4, Multer, Axios               |
| Тесты       | Jest + Supertest (API), Vitest + RTL (UI)          |
| ML          | HuggingFace Inference API (`nateraw/food`)         |
| CI/CD       | GitHub Actions                                     |
| Хостинг     | Vercel (фронт), Render (бэк)                       |

## REST API

| Метод | Путь                     | Описание                                                |
| ----- | ------------------------ | ------------------------------------------------------- |
| GET   | `/api/health`            | Health-check, используется Render                       |
| GET   | `/api/foods`             | Полная база продуктов                                   |
| GET   | `/api/foods/:label`      | Поиск и расчёт по названию (query: `portion`)           |
| POST  | `/api/analyze`           | multipart/form-data: `image` + `portion` → анализ фото  |

Пример ответа `/api/analyze`:

```json
{
  "label": "pizza",
  "confidence": 0.95,
  "nutrition": {
    "name": "Пицца",
    "matched": true,
    "calories": 532,
    "protein": 22,
    "fat": 20,
    "carbs": 66,
    "portionSize": 200
  },
  "recommendation": {
    "level": "warning",
    "text": "Высококалорийное блюдо. Подходит для основного приема пищи."
  }
}
```

## Локальный запуск

### 1. Backend

```bash
cd server
cp .env.example .env
# вставьте HF_TOKEN (получить на https://huggingface.co/settings/tokens)
npm install
npm run dev
```

API стартует на `http://localhost:4000`.

### 2. Frontend

```bash
cd client
cp .env.example .env
npm install
npm run dev
```

UI на `http://localhost:5173`.

### 3. Тесты

```bash
cd server && npm test        # Jest + Supertest
cd client && npm test        # Vitest
```

## Как всё задеплоить — пошагово

### Шаг 1. Создаём GitHub-репозиторий

```bash
cd CalorieScan
git add .
git commit -m "feat: full-stack CalorieScan (React + Express + CI/CD)"
git branch -M main
git remote add origin https://github.com/<your-username>/CalorieScan.git
git push -u origin main
```

### Шаг 2. Получаем HuggingFace токен

1. Заходим на https://huggingface.co и регистрируемся.
2. Settings → Access Tokens → **New token** (Read).
3. Копируем токен (выглядит как `hf_...`).

### Шаг 3. Деплоим backend на Render

1. Регистрируемся на https://render.com (можно через GitHub).
2. Dashboard → **New +** → **Web Service** → выбираем свой репозиторий.
3. Настройки:
   - **Name**: `caloriescan-api`
   - **Root Directory**: `server`
   - **Runtime**: Node
   - **Build Command**: `npm install`
   - **Start Command**: `node src/index.js`
   - **Plan**: Free
4. Вкладка **Environment** → добавляем переменные:
   - `HF_TOKEN` = ваш токен с HuggingFace
   - `HF_MODEL` = `nateraw/food`
   - `CORS_ORIGIN` = URL вашего фронта с Vercel (пока можно поставить `*`, потом заменить)
   - `NODE_ENV` = `production`
5. **Create Web Service** → ждём первый деплой.
6. Запоминаем URL вида `https://caloriescan-api.onrender.com`.
7. Вкладка **Settings** → **Deploy Hook** → копируем URL. Он понадобится для GitHub Actions.

> Альтернатива: можно зафиксировать инфраструктуру через `render.yaml` (уже лежит в корне) —
> тогда в Render при создании Blueprint подтянутся все параметры автоматически.

### Шаг 4. Деплоим frontend на Vercel

1. Регистрируемся на https://vercel.com через GitHub.
2. **Add New** → **Project** → импортируем репозиторий.
3. Настройки:
   - **Framework Preset**: Vite
   - **Root Directory**: `client`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. **Environment Variables** → добавляем:
   - `VITE_API_URL` = URL бэкенда с Render (например `https://caloriescan-api.onrender.com`)
5. **Deploy** → получаем URL вида `https://caloriescan.vercel.app`.
6. Возвращаемся в Render → меняем `CORS_ORIGIN` на этот URL → Save (Render передеплоит).

### Шаг 5. Прокидываем секреты в GitHub (для CI/CD авто-деплоя)

В GitHub: **Settings → Secrets and variables → Actions → New repository secret**. Добавляем:

| Секрет                   | Откуда взять                                                               |
| ------------------------ | -------------------------------------------------------------------------- |
| `RENDER_DEPLOY_HOOK_URL` | Render → Web Service → Settings → Deploy Hook                              |
| `VERCEL_TOKEN`           | Vercel → Account Settings → Tokens → Create                                |
| `VERCEL_ORG_ID`          | `vercel link` локально → `.vercel/project.json` → `orgId`                  |
| `VERCEL_PROJECT_ID`      | `vercel link` локально → `.vercel/project.json` → `projectId`              |

Как получить `VERCEL_ORG_ID` и `VERCEL_PROJECT_ID`:

```bash
cd client
npx vercel login
npx vercel link        # выбираем ваш проект
cat .vercel/project.json
```

### Шаг 6. Проверяем пайплайн

Делаем любой коммит и пушим в `main`:

```bash
git commit --allow-empty -m "chore: trigger CI"
git push
```

В GitHub → **Actions** должен запуститься workflow `CI/CD` с джобами:

1. **test-backend** — Jest прогон API.
2. **test-frontend** — Vitest прогон UI + production build.
3. **deploy-backend** — POST на Render Deploy Hook (только если оба теста зелёные).
4. **deploy-frontend** — Vercel CLI: pull → build → deploy prebuilt (только если оба теста зелёные).

Если тесты падают — деплой автоматически отменяется.

## Environment variables — сводка

### Backend (`server/.env`)

| Переменная    | Обязат.  | Описание                                            |
| ------------- | -------- | --------------------------------------------------- |
| `PORT`        | нет      | Порт Express (Render подставляет автоматически)     |
| `NODE_ENV`    | нет      | `development` / `production` / `test`               |
| `HF_TOKEN`    | **да**   | HuggingFace Access Token                            |
| `HF_MODEL`    | нет      | По умолчанию `nateraw/food`                         |
| `CORS_ORIGIN` | нет      | Разрешённые origin (через запятую) или `*`          |

### Frontend (`client/.env`)

| Переменная     | Обязат. | Описание                              |
| -------------- | ------- | ------------------------------------- |
| `VITE_API_URL` | **да**  | Base URL бэкенда (например Render)    |

### GitHub Actions Secrets

| Секрет                   | Зачем                             |
| ------------------------ | --------------------------------- |
| `RENDER_DEPLOY_HOOK_URL` | Авто-деплой backend после тестов  |
| `VERCEL_TOKEN`           | Авто-деплой frontend              |
| `VERCEL_ORG_ID`          | Идентификация Vercel организации  |
| `VERCEL_PROJECT_ID`      | Идентификация Vercel проекта      |

## Замечания

- **Render free tier** «засыпает» после 15 минут без активности — первый запрос после простоя
  может занять ~30 секунд. Для демонстрации это норма.
- **HuggingFace Inference API** бесплатный с rate limits. Для продакшена стоит перейти на
  платный план или поднять модель в HF Spaces.
- База продуктов лежит в `server/src/data/foodDatabase.js` — ~140 позиций с переводами и БЖУ.
