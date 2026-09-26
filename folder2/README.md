# E-Commerce Automated Testing Framework

An automated end-to-end regression testing framework built with **Python**, **Selenium WebDriver**, and **PyTest** to validate the core shopping workflow on an e-commerce platform ([TutorialsNinja Demo](https://tutorialsninja.com/demo/)).

---

## 📌 Features

- **Modular Architecture**: Separate directories for test logic, configuration data, screenshots, and execution reports.
- **Dynamic Synchronization**: Utilizes explicit waits (`WebDriverWait` and `ExpectedConditions`) to prevent flaky test runs.
- **Externalized Test Data**: Input values (URLs, credentials, search terms) are managed independently in `data/test_data.py`.
- **Automated Reporting**: Generates standalone, self-contained HTML reports (`pytest-html`) showing detailed test outcomes and execution metadata.
- **Visual Evidence**: Automatically captures step-by-step PNG screenshots during execution, along with dynamic failure-snapshot capturing via PyTest hooks.

---

## 🛠️ Technology Stack & Dependencies

- **Language**: Python 3.x
- **Browser Automation**: Selenium WebDriver
- **Test Framework**: PyTest
- **Reporting**: PyTest-HTML
- **Driver Management**: Webdriver-Manager

---

## 📁 Project Structure

```text
selenium_capstone_project/
├── data/
│   ├── __init__.py         # Package declaration
│   └── test_data.py        # Centralized test parameters & configuration
├── reports/                # Output directory for HTML test execution reports
├── screenshots/            # Step-by-step PNG screenshot output directory
├── conftest.py             # PyTest fixtures for driver lifecycle & failure hooks
├── test_e2e_shopping.py    # Main Selenium automation test script
├── .gitignore              # Specifies intentionally untracked files to ignore
└── README.md               # Project documentation