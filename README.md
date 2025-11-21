## Development Environment Setup

Follow these steps to set up and run the project in a development environment.

### Prerequisites

*   Docker and Docker Compose
*   Python 3.x
*   Git

### Backend Setup

1. **Create a Python Virtual Environment:**
    It is recommended to use a virtual environment to manage your project's dependencies independently.
    ```bash
    python -m venv venv
    ```

2. **Activate the Virtual Environment:**
    *   **On Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

3. **Install Python Dependencies:**
    With your virtual environment activated, install all required packages from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4. **Start the Database:**
    Use Docker Compose to start the database service.
    ```bash
    docker-compose up -d
    ```

5. **Run Database Migrations:**
    Apply the database migrations to set up the schema using the command format mentioned above.
    ```bash
    python manage.py migrate
    ```

6. **Run the Development Server:**
    Start the Django development server using the same `PYTHONPATH` setup.
    ```bash
    python manage.py runserver
    ```

### Frontend Setup

The frontend code is included as a Git submodule.

To initialize and fetch the frontend code, run the following command from the root of the `open_schools_marketplace_backend` directory:

```bash
git submodule update --init
```
---