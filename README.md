# FlaskStuct

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
   git clone <repository-url>
   cd flaskstuct
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Copy the example environment file and fill in your details:
   ```bash
   cp .env.example .env
   ```

5. **Run the development server:**
   ```bash
   # On Windows PowerShell:
   .\venv\Scripts\python run.py
   # On Bash/WSL:
   ./venv/bin/python run.py
   ```

## Running Tests
To run the test suite via WSL:
```bash
wsl ./venv/bin/python -m pytest
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
