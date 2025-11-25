# Chorogrami
# 🐳 Development Environment (Docker)

This project is fully containerized. You don't need to install Python, dependencies, or configure a database locally. Everything starts with a single command.

## 🛠 Requirements

1.  Install **Docker Desktop**: [Download here]( https://www.docker.com/products/docker-desktop/ )  
2.  Launch Docker Desktop and make sure it's running in the background.

---

## 🚀 Quick Start

1.  Open terminal in the main project directory.
2.  Start the environment:
    ```bash
    docker-compose up --build
    ```
3.  Wait until you see in the logs:
    * `Application startup complete` (Backend)
    * `You can now view your Streamlit app in your browser` (Frontend)
  

### 🔗 Application URLs:

* **Frontend (Streamlit):** [http://localhost:8051](http://localhost:8051)
* **Backend (API Documentation):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 👨‍💻 How to Work (Development Workflow)

Thanks to configured volumes, you don't need to restart Docker after every code change.

1.  **Code editing:** Open the project in your IDE (VS Code / PyCharm).
2.  **Save file:** After pressing `Ctrl+S`, Docker will automatically detect the change.
3.  **Hot Reload:**
    * **Frontend:** Refresh the page in browser (or click 'Rerun' in Streamlit).
    * **Backend:** Server will reload automatically.

### 📦 Adding New Libraries

We use the **`uv`** package manager. If you add a new library (e.g., `uv add numpy`), you need to rebuild the image for Docker to "see" it.

1.  Add the library locally (to update `pyproject.toml` and `uv.lock` files):
    ```bash
    cd backend  # or frontend
    uv add library_name
    ```
2.  Rebuild containers:
    ```bash
    cd ..
    docker-compose up -d --build
    ```

---

## 🚒 Troubleshooting

### 1. Error: "Port is already allocated"
You have something else running on port 8000 or 8051 (maybe an old Python process?).
* **Solution:** Stop other applications or run: `docker-compose down`, then try again.

### 2. Frontend doesn't connect to Backend
Remember: Inside Docker **we don't use `localhost`** for communication between containers.
* Frontend connects to backend at: `http://backend:8000`.
* This variable is set automatically in `docker-compose.yml` (`BACKEND_URL`). Don't hardcode it in the code!

### 3. Database (SQLite)
The database is a `database.db` file in the `backend/` folder.
* It's mapped from your disk. If you remove the container (`down`), data **won't be lost**.
* If you want to clear the database: delete the `database.db` file manually and restart the backend.

---

## 📜 Command Cheatsheet

| Command | What does it do? |
| :--- | :--- |
| `docker-compose up` | Starts everything and shows logs (Ctrl+C to exit) |
| `docker-compose up -d` | Starts everything in background (you can close terminal) |
| `docker-compose down` | Stops and removes containers (cleanup) |
| `docker-compose logs -f` | Live log viewing |
| `docker-compose up --build` | Forces rebuild (e.g., after adding libraries) |
| `docker system prune` | If Docker takes too much disk space (cleans up garbage) |
