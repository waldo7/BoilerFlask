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

## Project Structure
To help you navigate, here is a quick breakdown of how BoilerFlask is organized:
* **`app/`**: The main application folder containing all your code.
  * **`main/` & `auth/`**: Blueprints (modules) that separate your core pages from your authentication logic.
  * **`models/`**: Database models defining your tables (using SQLAlchemy).
  * **`templates/`**: HTML files (Jinja templates) that define your frontend.
  * **`static/`**: CSS, JavaScript, and images.
* **`config.py`**: Defines different environments (Development, Testing, Production).
* **`extensions.py`**: Where Flask extensions (Database, Login Manager) are initialized to avoid circular imports.

## Understanding Configuration
It is important to keep your secrets secure! That's why BoilerFlask uses environment variables.
* **`config.py`**: This file loads settings into Flask. **Never put real passwords in here!**
* **`.env`**: This is where you put your actual secrets (like database URLs or API keys). This file is ignored by Git, so your secrets never get uploaded to GitHub.
* **`.env.example`**: A safe template file that you *do* upload to GitHub to show other developers what variables they need to fill in.

## Customizing Your App
To rebrand BoilerFlask and start building your own features, check out these key files:
* **Project Name:** Search and replace "BoilerFlask" in `config.py` and the HTML templates (like `app/templates/base.html` and `app/templates/marketing_base.html`).
* **Routes & Pages:** Add your new pages and logic in `app/main/routes.py`.
* **Database Models:** Define your new database tables in the `app/models/` folder.
* **Styling:** Add your custom CSS to `app/static/css/app.css`.

## Contributing & Support
If you want to contribute to the project, the process is simple!
1. **Fork** the repository on GitHub.
2. **Clone** your fork locally and create a new branch (`git checkout -b my-new-feature`).
3. **Commit** your changes and push the branch to your fork.
4. **Submit a Pull Request** (PR) to the `main` repository so we can review it!

If you find a bug or have a feature idea, please open an **Issue** on the GitHub repository.

## Running Tests
To run the test suite:
* **Windows:** `.\venv\Scripts\python -m pytest`
* **Mac/Linux:** `./venv/bin/python -m pytest`

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
