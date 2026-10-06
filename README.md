# AI Team Backend API

A Python backend API that provides document management and AI-powered search functionality. The API is built with **FastAPI** and provides interactive Swagger documentation for testing the available endpoints.

## 🚀 Features

* Upload and store documents
* Get document details
* Search documents
* Download documents
* Delete documents
* AI-powered question/answer endpoint
* REST API architecture
* Interactive Swagger UI
* Easy integration with frontend and other teams

## 🛠️ Technologies

* Python
* FastAPI
* Uvicorn
* SQLite / Database
* REST API
* Swagger / OpenAPI

## 📁 Main API Functions

| Method | Endpoint                       | Description           |
| ------ | ------------------------------ | --------------------- |
| GET    | `/documents/{doc_id}`          | Get a document by ID  |
| GET    | `/documents/search`            | Search documents      |
| GET    | `/documents/{doc_id}/download` | Download a document   |
| POST   | `/documents/upload`            | Upload a document     |
| DELETE | `/documents/{doc_id}`          | Delete a document     |
| POST   | `/ask`                         | Ask the AI a question |

> **Note:** The exact endpoint names may vary depending on the current backend implementation.

## ▶️ Run the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI server

```bash
uvicorn main:app --reload
```

The API will normally run at:

```text
http://127.0.0.1:8000
```

## 📖 Swagger UI

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows developers to test the API endpoints directly from the browser.

## 🔍 API Testing

The backend can be tested using Swagger UI or an API client such as Postman.

Example:

```text
GET /documents/1
```

This returns the document with ID `1`.

## 🤖 AI Endpoint

The AI team can communicate with the backend through the AI question endpoint.

Example:

```text
POST /ask
```

Example request:

```json
{
  "question": "What are the company rules?"
}
```

The endpoint processes the question and returns an AI-generated response based on the available information.

## 🔗 Integration

The backend API can be integrated with:

* AI services
* Frontend applications
* Cybersecurity testing
* Document management systems
* Other internal services

For local development, the API is available through the FastAPI server.

## 🔐 Security

Security testing should be performed before deploying the API publicly.

Recommended checks include:

* Authentication and authorization
* Input validation
* File upload validation
* SQL injection protection
* Rate limiting
* Secure API configuration
* CORS configuration
* Sensitive information protection

## 📌 Project Status

**Status:** Development / Testing

The API endpoints are being tested and prepared for integration with the AI and cybersecurity teams.

## 👩‍💻 Backend Developer

**Rubab Akber Lodhi**

Python Backend Developer
FastAPI | REST API | SQLite | Python

---

### 📄 License

This project is intended for educational and team development purposes.

