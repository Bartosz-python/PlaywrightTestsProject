# Playwright Tests Project

Automated testing framework built with **Python**, **Pytest**, and **Playwright**, designed for testing web UI and APIs.  
The project supports **data-driven testing**, **multi-browser execution**, and **BDD (Cucumber/Gherkin)**-style scenarios.  
Target application under test: **[https://rahulshettyacademy.com/client](https://rahulshettyacademy.com/client)**

---

## 📁 Project Structure

```
PLAYWRIGHTTESTSPROJECT/
│
├── data/               # JSON test data (e.g., credentials, payloads)
├── features/           # Gherkin feature files (BDD scenarios)
├── tests/              # Pytest test cases (UI + API)
├── utils/              # Page objects, fixtures, and helper functions
│
├── .env                # Environment variables (URLs, secrets, etc.)
├── .gitignore
├── LICENSE
├── conftest.py         # Global fixtures and CLI options (--browser_name, etc.)
├── pytest.ini          # Pytest configuration
├── requirements.txt    # Dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Bartosz-python/PlaywrightTestsProject.git
cd PlaywrightTestsProject
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install
```

---

## 🧪 Running Tests

### Run all tests
```bash
pytest
```

### Run feature (BDD) tests
```bash
pytest features/
```

### Run tests with detailed tracebacks
```bash
pytest -tb=long
```

### Run tests on a specific browser
You can choose which browser Playwright uses via a **custom CLI argument** defined in `conftest.py`.

```bash
pytest --browser_name chromium
pytest --browser_name firefox
pytest --browser_name webkit
```

Default browser: `chromium`

---

## 🧩 Test Data

All reusable test data (like user credentials, API payloads, etc.) lives in `/data` as JSON files.

Example:
```json
{
  "valid_user": {
    "email": "test_user@example.com",
    "password": "Password123!"
  }
}
```
---

## 📊 Reports

After every test run, reports are generated automatically (e.g. **Allure**, **pytest-html**).

Example (Allure):
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

Example (pytest-html):
```bash
pytest --html=reports/report.html --self-contained-html
```

---

## 🌐 Target Page

All UI tests target:
> [https://rahulshettyacademy.com/client](https://rahulshettyacademy.com/client)

Base URL can be configured in `.env` or via `pytest.ini`:
```ini
[pytest]
base_url = https://rahulshettyacademy.com/client
```

---

## 💡 Features

- ✅ UI testing with **Playwright**
- ✅ API testing via Playwright or `requests`
- ✅ Data-driven testing using JSON files
- ✅ Gherkin syntax for readable BDD scenarios
- ✅ Cross-browser testing (`--browser_name`)
- ✅ Configurable test reports (HTML / Allure)
- 🚧 CI/CD pipeline integration planned

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Playwright**
- **Pytest**
- **pytest-bdd** (for Gherkin)
- **pytest-html** / **Allure-pytest** (for reporting)

---

## ⚖️ License

This project is licensed under the MIT License – see [LICENSE](./LICENSE) for details.