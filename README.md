# BoilerFlask

A production-ready, organized Flask foundation with authentication and a responsive UI out of the box.

## Features
- **App Factory Pattern**: Clean application initialization and configuration.
- **Blueprint Architecture**: Scalable structure with domain-specific routing (`main`, `auth`).
- **Database Integrated**: SQLAlchemy setup with SQLite for dev and Postgres/MySQL ready for production.
- **Authentication**: Built-in authentication boilerplate.
- **UI Framework**: Integrated with Bootstrap 5 and Jinja template inheritance (`base.html`).

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/waldo7/BoilerFlask.git
   cd BoilerFlask
   ```

2. **Create a virtual environment:**
   * **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     ```
   * **Mac / Linux:**
     ```bash
     python3 -m venv venv
     ```

3. **Install dependencies:**
   * **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\pip install -r requirements.txt
     ```
   * **Mac / Linux:**
     ```bash
     ./venv/bin/pip install -r requirements.txt
     ```

4. **Environment Variables:**
   Copy the example environment file:
   * **Windows (PowerShell):**
     ```powershell
     Copy-Item .env.example .env
     ```
   * **Mac / Linux:**
     ```bash
     cp .env.example .env
     ```

5. **Run the development server:**
   * **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\python run.py
     ```
   * **Mac / Linux:**
     ```bash
     ./venv/bin/python run.py
     ```
   *(Note: The development server automatically creates your SQLite database and tables when you first run it!)*

## Admin Setup
To create an initial admin user to access secure areas of your app, run:
* **Windows:** `.\venv\Scripts\flask create-admin`
* **Mac/Linux:** `./venv/bin/flask create-admin`

## Running Tests
To run the test suite:
* **Windows:** `.\venv\Scripts\python -m pytest`
* **Mac/Linux:** `./venv/bin/python -m pytest`

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
