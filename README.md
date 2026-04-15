# Biz Task Tracker

**Biz Task Tracker** is a modern Full-stack system designed for small businesses to automate request intake and eliminate operational chaos. Built with **Python**, it leverages an asynchronous stack for maximum performance and reliability.


---

## Key Features

* ⚡ **Async-first Backend**: High-performance architecture powered by **FastAPI** and **SQLAlchemy 2.0**.
* 🛡️ **Robust Validation**: Strict data integrity using **Pydantic V2** for schema enforcement.
* 🏗️ **Clean Architecture**: Implementation of the **Repository Pattern** to decouple business logic from database operations.
* 👥 **User Management**: Integrated role tracking and relational mapping between task creators and assignments.
* 🤖 **AI Powered (WIP)**: Planned **RAG (Retrieval-Augmented Generation)** system for natural language querying of task history.
* 📱 **Multi-interface**: Currently developing a **Frontend dashboard** and a **Telegram bot** for seamless cross-platform management.

---

## Interactive API Documentation

Once the project is running, you can access:

* **Swagger UI**: An interactive playground to test all endpoints.
* **ReDoc**: Alternative structured API documentation.

# <a href="https://storied-rugelach-0a138f.netlify.app/" target="_blank"> Swagger API Demo </a>

---

## Technical Stack

### Backend
* **Python 3.10+**: The core programming language.
* **FastAPI**: Modern web framework for building APIs.
* **SQLAlchemy**: Database ORM with asynchronous `asyncpg` support.
* **Pydantic**: Data validation and settings management.

### Frontend (In Development)
* **HTML5 & CSS3**: For building responsive and user-friendly interfaces.

---

## Project Structure

The repository follows a modular layout to ensure scalability:

* `main.py`: Entry point, application initialization, and API routing.
* `models.py`: SQLAlchemy database models and table definitions.
* `schemas.py`: Pydantic schemas for request/response validation.
* `repository.py`: Data access layer for CRUD operations.
* `database.py`: Database engine configuration and async session management.

---

## Getting Started

### 1. Environment Configuration
Create a `.env` file in the root directory and specify your database URL:

```bash
SQLALCHEMY_DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/db_name"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Server
```bash
uvicorn main:app --reload
```

---

## Development Status (Roadmap)

This project is currently **Work in Progress**.

* [x] Core API architecture and asynchronous DB integration.
* [x] Repository Pattern implementation.
* [ ] Frontend Dashboard development (HTML/CSS).
* [ ] RAG System integration for AI-driven insights.
* [ ] Telegram Bot interface launch.

---

## Contact

**LinkedIn**: [Danylo Blidar](https://pl.linkedin.com/in/danylo-blidar-4416bb365)  

---

### 🚧 Final Note
**This repository is under active development.** I am currently refining the core architecture and adding features to move from a basic CRUD system to a production-ready business tool. My focus is on the **AI Assistant (RAG)** and **Telegram integration** to provide a seamless experience for small business owners.
