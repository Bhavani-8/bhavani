# 🚀 Selenium Automation Testing Framework

This framework is designed for automating web application testing using **Python**, **Selenium**, **PyTest**, and **Allure Reports**. It is modular, data-driven, and easy to extend.

---

## 📦 Setup Instructions

Before running tests, you must install the necessary dependencies and tools.

### ✅ Step 1: Run the Setup Script

Use the provided batch script to automate installation:

```bash
setup_framework.bat
```

This script will:

- ✅ Install Python packages from `requirements.txt`
- 🥄 Install Scoop (if not already installed)
- ✨ Install Allure CLI via Scoop
- 📌 Display the installed Allure version

> 📝 The script checks for existing installations and won’t re-install them unnecessarily.

---

### 🚨Follow these steps if the .bat script doesn’t work or if you prefer to install manually.

- 🐍 Install Python Packages: 
Make sure you are in the root project folder and run:

```bash
pip install -r requirements.txt
```

#### 🥄 Install Scoop (Windows Package Manager)
Open PowerShell and run:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Then install Scoop:

```powershell
iwr -useb get.scoop.sh | iex
```

#### ⚠️ If Scoop gives a Git error, install Git first:

```powershell
scoop install git
```

#### ✨ Install Allure CLI using Scoop Once Scoop is installed:

```powershell
scoop install allure
```

#### 📌 Verify Allure Installation Check the installed version:

```powershell
allure --version
```
---

## 🧪 Running Tests

### 📁 Step 2: Configure Your Tests in `test_data.json`

Located in the `data/` folder, this file controls what tests to run and on which browser.

**Example:** For simple test cases like positive or negative cases

```json
{
  "browser": "chrome",
  "modules_to_test": {
    "login": ["positive", "negative"],
    "forgot_password": ["all"]
  }
}
```

**Example:** For specific tests cases like smoke or regression

```json
{
  "browser": "chrome",
  "modules_to_test": "smoke"
  }
}
```

- `"browser"`: Supports `chrome`, `firefox`, or `edge`
- `"modules_to_test"`: Define which test suites and test types to run (e.g., positive, negative, or all)

---

### 🧾 Step 3: Maintain Test Cases in Excel

Your test cases for each module (e.g., login, signup) live in dedicated sheets inside `test_data.xlsx`.

#### 🔐 Login Test Case Sheet Example

| username         | password   | expected_success | level_of_testing    |
|------------------|------------|------------------|---------------------|
| test@test.com    | Test@123   | true             | smoke,regression    |
| wrong@test.com   | Test@124   | false            | regression          |
| test@test.com    | Test@125   | false            | regression          |
| test@test.com    | Wrong@126  | false            | regression          |
| wrong@test.com   | Wrong@127  | false            | smoke,regression    |

> ✅ The `level_of_testing` column allows filtering test cases dynamically based on `smoke`, `regression`, or other tags.

#### ❗ Note:

- Multiple levels can be comma-separated (e.g., `smoke,regression`).

---

### ▶️ Step 4: Run the Framework

Once the test data is configured, execute:

```bash
python runner.py
```

This will:

- Load test config from `test_data.json`
- Run selected test cases using `pytest`
- Generate Allure reports under `reports/allure-results`
- Automatically open the report in your browser

---

## 📊 Viewing Allure Reports Again (Optional)

If you want to re-open the previously generated report:

```bash
allure serve reports/allure-results
```

Make sure Allure is installed via Scoop.

---

## 📁 Folder Structure

```bash
automation_framework/
│
├── data/
│   └── Test configuration and test cases(excel or json)
│
├── reports/
│   └── allure-results/            # Allure report output directory
│   └── allure-report/            # Allure report output directory
│
├── tests/
│   ├── Code files for test cases
│
├── utilities/
│   ├── Browser driver setup
│   ├── Supporting code files for test cases
│
├── runner.py                      # Main test runner
├── requirements.txt               # Python package dependencies
└── setup_framework.bat           # One-click setup script
```

---
