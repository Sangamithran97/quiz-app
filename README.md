# Quizzy — AI-Powered Quiz API

A comprehensive REST API for a quiz application that handles user management, AI-powered quiz generation, and detailed analytics. Built with Django and Django REST Framework, powered by Google Gemini AI.

## Live API

**Web URL**: `https://quiz-app-17ly.onrender.com/swagger/`  

---

## Tech Stack

- **Backend**: Django 5.x, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (via djangorestframework-simplejwt)
- **AI Integration**: Google Gemini-3-flash-preview
- **Documentation**: Swagger UI (drf-yasg)
- **Deployment**: Render

---

## Local Setup

### Prerequisites

- Python 3.10+
- PostgreSQL installed and running
- Google Gemini API key (get one free at https://aistudio.google.com/apikey)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Sangamithran97/quiz-app.git
cd quiz-app
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create PostgreSQL database**
```bash
psql -U postgres -h localhost
CREATE DATABASE quiz_app_db;
\q
```

**5. Create `.env` file** in the project root:
```
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=quiz_app_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
GEMINI_API_KEY=your-gemini-api-key
```

**6. Run migrations**
```bash
python manage.py migrate
```

**7. Create a superuser (optional)**
```bash
python manage.py createsuperuser
```

**8. Start the server**
```bash
python manage.py runserver
```

**9. Open Swagger UI**
```
http://127.0.0.1:8000/swagger/
```

---

## Database Schema

### Models and Relationships

```
User (accounts)
├── id, username, email, password, role (admin/user)
└── has many → Attempts

Quiz (quizzes)
├── id, topic, difficulty, question_count, created_at
├── created_by → User (FK)
└── has many → Questions, Attempts

Question (quizzes)
├── id, question_text, options (JSON), correct_answer
└── belongs to → Quiz (FK)

Attempt (attempts)
├── id, score, started_at, completed_at
├── user → User (FK)
├── quiz → Quiz (FK)
└── has many → Answers

Answer (attempts)
├── id, selected_answer, is_correct
├── attempt → Attempt (FK)
└── question → Question (FK)
```

### Relationships Summary

- A **User** can create many **Quizzes** and make many **Attempts**
- A **Quiz** has many **Questions** and can have many **Attempts**
- An **Attempt** belongs to one **User** and one **Quiz**, and has many **Answers**
- An **Answer** belongs to one **Attempt** and one **Question**

---

## API Endpoints

### Authentication — `/api/accounts/`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/accounts/register/` | Register a new user | No |
| POST | `/api/accounts/login/` | Login and get JWT tokens | No |
| POST | `/api/accounts/refresh/` | Refresh access token | No |

**Register request body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword",
  "role": "user"
}
```

**Login response:**
```json
{
  "access": "eyJhbGci...",
  "refresh": "eyJhbGci..."
}
```

---

### Quizzes — `/api/quizzes/`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/quizzes/create/` | Generate AI quiz | Yes |
| GET | `/api/quizzes/` | List all quizzes | Yes |
| GET | `/api/quizzes/<id>/` | Get quiz with questions | Yes |
| DELETE | `/api/quizzes/<id>/manage/` | Delete a quiz (admin only) | Yes (Admin) |

**Create quiz request body:**
```json
{
  "topic": "Python Programming",
  "difficulty": "medium",
  "question_count": 5
}
```

> `difficulty` must be one of: `easy`, `medium`, `hard`  
> `question_count` must be between 1 and 20

---

### Attempts — `/api/attempts/`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/attempts/start/` | Start a quiz attempt | Yes |
| POST | `/api/attempts/submit/` | Submit answers and get score | Yes |
| GET | `/api/attempts/<id>/review/` | Review attempt with correct answers | Yes |

**Start attempt request body:**
```json
{
  "quiz_id": 1
}
```

**Submit attempt request body:**
```json
{
  "attempt_id": 1,
  "answers": [
    {"question_id": 1, "selected_answer": "Paris"},
    {"question_id": 2, "selected_answer": "Python"}
  ]
}
```

**Submit response:**
```json
{
  "score": 4,
  "total": 5,
  "message": "Attempt submitted"
}
```

---

### Analytics — `/api/analytics/`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/analytics/performance/` | Overall stats for current user | Yes |
| GET | `/api/analytics/history/` | Paginated quiz history | Yes |

**Performance response:**
```json
{
  "total_quizzes": 10,
  "total_score": 42,
  "average_score": 4.2
}
```

**History response (paginated):**
```json
{
  "count": 10,
  "next": "http://...?page=2",
  "previous": null,
  "results": [
    {
      "attempt_id": 1,
      "quiz_topic": "Python Programming",
      "score": 4,
      "total_questions": 5,
      "completed_at": "2026-03-20 14:30"
    }
  ]
}
```

---

## Authentication Flow

This API uses JWT (JSON Web Token) authentication.

1. Register or login to receive an `access` token and `refresh` token
2. Include the access token in the `Authorization` header for all protected endpoints:
```
Authorization: Bearer eyJhbGci...
```
3. Access tokens expire after **60 minutes**
4. Use the refresh token at `/api/accounts/refresh/` to get a new access token without logging in again

---

## Role-Based Permissions

| Role | Can Do |
|------|--------|
| `user` | Register, login, create quizzes, attempt quizzes, view own analytics |
| `admin` | Everything a user can do + delete any quiz |

Set the role during registration by passing `"role": "admin"` or `"role": "user"`.

---

## Rate Limiting & Throttling

To prevent API abuse and control AI service costs:

- **Global user rate limit**: 15 requests/day per user
- **Quiz creation burst limit**: 2 requests/minute per user

This is especially important for quiz creation since each request calls the Gemini AI API.

---

## AI Integration

Quiz questions are generated dynamically using **Google Gemini 3 Flash Preview**.

### How it works

1. User sends a POST request to `/api/quizzes/create/` with topic, difficulty, and question count
2. The API constructs a prompt and sends it to Gemini
3. Gemini returns a JSON list of questions with options and correct answers
4. Questions are validated, saved to the database, and returned to the user

### Prompt Design

```
Generate {count} multiple-choice questions about {topic} at a {difficulty} level.
Return the response ONLY as a JSON list of objects with these keys:
"question_text", "options" (a list of 4 strings), and "correct_answer" (must be one of the options).
Do not include markdown formatting like ```json.
```

### Failure Handling

If the AI service fails (quota exceeded, network error, invalid response), the API returns a `503 Service Unavailable` with a clear error message rather than crashing.

---

## Design Decisions & Trade-offs

### Why JWT over Session Authentication?
JWT is stateless — the server doesn't need to store session data. This makes the API easier to scale horizontally and works well for mobile/frontend clients that need to store tokens locally.

### Why PostgreSQL over SQLite?
PostgreSQL handles concurrent connections, supports JSON fields natively (used for question options), and is production-grade. SQLite is fine for development but not suitable for a deployed API.

### Why separate Attempt and Answer models?
Separating them allows detailed per-question analytics. You can track not just the final score but exactly which questions a user got wrong, enabling the attempt review endpoint to return detailed feedback.

### Question ownership validation
When submitting answers, the API validates that every submitted `question_id` belongs to the quiz of the current attempt. This prevents users from submitting answers for questions from a different quiz and manipulating their scores.

### Re-submission prevention
Once an attempt has a `completed_at` timestamp, it cannot be submitted again. This prevents score manipulation by submitting multiple times.

---

## Challenges & Solutions

**Challenge**: Gemini sometimes returns questions wrapped in markdown code fences (` ```json `) despite being told not to.  
**Solution**: Added a post-processing step that strips markdown formatting before JSON parsing.

**Challenge**: The `google-generativeai` package was deprecated mid-development.  
**Solution**: Evaluated the new `google-genai` package but reverted to the old one due to API version compatibility issues with available model names. The deprecation warning is acknowledged and migration is planned.

**Challenge**: Swagger UI doesn't auto-detect request bodies for `APIView` classes.  
**Solution**: Used `@swagger_auto_schema` decorator with explicit `openapi.Schema` definitions on all POST endpoints.

**Challenge**: PostgreSQL PATH configuration on Windows during local development.  
**Solution**: Used `dj_database_url` which accepts a single `DATABASE_URL` environment variable, simplifying both local and production database configuration.

---

## Testing Approach

API endpoints were tested manually using:
- **Swagger UI** at `/swagger/` for interactive testing
- **Thunder Client** (VS Code extension) for raw request testing

### Test Scenarios Covered

- User registration with valid and invalid data
- Login and token refresh flow
- Quiz creation with valid/invalid difficulty and question count
- Starting and submitting an attempt
- Submitting an already completed attempt (should return 400)
- Submitting answers with questions from a different quiz (should return 400)
- Analytics endpoints with no attempts (should return zeros)
- Paginated history endpoint

---

## Project Structure

```
quiz-app/
├── config/
│   ├── settings.py       # Django settings
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py
├── accounts/
│   ├── models.py         # Custom User model
│   ├── serializers.py    # Registration serializer
│   ├── views.py          # Register view
│   ├── permissions.py    # IsAdmin permission class
│   └── urls.py
├── quizzes/
│   ├── models.py         # Quiz and Question models
│   ├── serializers.py    # Quiz and Question serializers
│   ├── views.py          # CRUD + AI generation views
│   ├── services.py       # Gemini AI integration
│   └── urls.py
├── attempts/
│   ├── models.py         # Attempt and Answer models
│   ├── views.py          # Start, submit, review views
│   └── urls.py
├── analytics/
│   ├── views.py          # Performance and history views
│   └── urls.py
├── requirements.txt
├── Procfile
├── manage.py
└── README.md
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for development, `False` for production |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL username |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | Database host |
| `DB_PORT` | Database port (default 5432) |
| `GEMINI_API_KEY` | Google Gemini API key |
| `DATABASE_URL` | Full database URL (used in production on Render) |