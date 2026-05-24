![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=java&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![TestNG](https://img.shields.io/badge/TestNG-red?style=for-the-badge)

# AI-Assisted QA Automation - PrestaShop Demo

## G+D Netcetera x FINKI Collaboration
This project was developed as part of a collaboration between **Netcetera** and the **Faculty of Computer Science & Engineering (FINKI)**, focused on applying AI in Quality Assurance and test automation workflows.

### Full Project Presentation: https://newqaprezv1.vercel.app

---

This project was developed as part of a collaboration between **G+D Netcetera** and the **Faculty of Computer Science & Engineering (FINKI)**, focused on applying Artificial Intelligence in Quality Assurance and automation testing workflows.

The goal of the collaboration is to explore the practical usage of AI tools in software testing processes, specifically in:
- Identifying automation opportunities
- Generating automation tests
- Comparing AI-assisted and human-written automation approaches
- Evaluating maintainability and scalability of generated automation code

The repository demonstrates how AI can support QA engineers during automation development while also highlighting the strengths and limitations of AI-generated automation solutions in real-world testing scenarios.

---

# Project Goals

The primary goals of this project are:

- Analyze Sprint 1 and Sprint 2 test cases and test charters
- Identify functionalities suitable for automation
- Compare AI-assisted and human-written automation implementations
- Evaluate maintainability and scalability of AI-generated code
- Improve automation development efficiency
- Maximize automation coverage for selected functionalities
- Explore AI integration in QA engineering workflows

The project also aims to evaluate whether AI-assisted automation can:
- Reduce implementation time
- Improve productivity
- Generate readable and maintainable automation code
- Support QA engineers during test development
- Maintain automation stability and accuracy

---

# 📖 About the Project

This repository contains automation tests created for the **PrestaShop Demo** web application.

The implemented test scenarios are based on:
- Sprint 1 test cases
- Sprint 2 test cases
- Exploratory test charters

The project workflow included:
1. Analysis of manual test cases
2. Identification of automation candidates using AI tools
3. Division of functionalities among team members
4. Development of automation tests
5. Comparison between human-written and AI-assisted automation solutions

For selected functionalities:
- One automation test was written completely manually
- Minimum two automation tests were generated or assisted using AI tools

The project focuses not only on creating functional automation tests, but also on evaluating:
- Test quality
- Readability
- Stability
- Reusability
- Long-term maintainability

---

# 🧪 Automation Approach

The automation strategy used in this project focuses on:
- Readable and maintainable test structure
- Reusable page objects and utility classes
- Separation of test logic and reusable components
- Comparison between different automation implementation approaches

The repository includes:
- Human-written automation tests
- AI-assisted automation tests
- Shared utilities and reusable methods
- Base test configuration
- Page Object Model implementation

The goal is to keep the project:
- Simple
- Scalable
- Understandable
- Easy to maintain

---

# 📂 Project Structure

```bash
project
├── docs
│   ├── comparisons
│   └── reviews
│
├── src
│   ├── main
│   │   └── java
│   │       ├── pages
│   │       └── utils
│   │
│   └── test
│       └── java
│           ├── base
│           └── tests
│               ├── checkout
│               │   ├── automated_ai
│               │   └── human_written
│               │
│               ├── error_handling
│               │   ├── automated_ai
│               │   └── human_written
│               │
│               ├── navigation
│               ├── product_details
│               ├── search_filter
│               ├── shopping
│               └── user_account
│
├── target
├── pom.xml
└── README.md
```

---

# 📁 Folder Overview

## `docs`
Contains additional project documentation.

### `comparisons`
Includes comparisons between human-written and AI-assisted automation tests based on:
- Maintainability
- Readability
- Stability
- Efficiency
- Accuracy

### `reviews`
Contains reviews and evaluations of implemented automation tests and project deliverables.

---

## `src/main/java`

### `pages`
Contains Page Object Model (POM) classes used for organizing web elements and reusable page actions.

### `utils`
Contains reusable utility classes and helper methods such as:
- WebDriver utilities
- Wait utilities
- Configuration helpers
- Common reusable actions

---

## `src/test/java`

### `base`
Contains shared base test setup and initialization logic used across all automation tests.

### `tests`
Contains all implemented automation test scenarios organized by functionality.

---

# 🧪 Test Organization

The automation tests are grouped based on application functionalities.

## `checkout`
Contains checkout-related automation tests.

### `automated_ai`
AI-assisted automation implementations for checkout functionality.

### `human_written`
Human-written automation implementations for checkout functionality.

---

## `error_handling`
Contains automation tests related to validations, negative scenarios, and error handling.

### `automated_ai`
AI-assisted implementations for error handling scenarios.

### `human_written`
Human-written implementations for error handling scenarios.

---

## `navigation`
Contains automation tests related to website navigation and menu functionality.

---

## `product_details`
Contains tests for product details pages and product-related validations.

---

## `search_filter`
Contains automation tests for product search and filtering functionalities.

---

## `shopping`
Contains shopping cart and shopping workflow automation tests.

---

## `user_account`
Contains automation tests related to:
- Login
- Registration
- User profile functionality
- Account management

---

# ⚙️ Technologies Used

The project was developed using the following technologies and tools:

- Java
- Selenium WebDriver
- TestNG
- Maven
- IntelliJ IDEA
- Git & GitHub
- AI-assisted development tools

---

# ⚙️ Setup Instructions

## Prerequisites

Before running the project locally, make sure you have installed:

- Java JDK 17 or newer
- Apache Maven
- IntelliJ IDEA (recommended)
- Google Chrome browser
- Git

---

# 📥 Clone the Repository

Clone the repository from GitHub:

```bash
git clone https://github.com/istevanoska/qa-automation.git
```

Navigate into the project folder:

```bash
cd qa-automation
```

---

# 📦 Install Dependencies

Install all required Maven dependencies:

```bash
mvn clean install
```

This command will:
- Download all required dependencies
- Build the project
- Verify Maven configuration

---

# ✔️ Running the Tests

## Run All Tests

To execute all automation tests:

```bash
mvn test
```

---

## Run Specific Test Class

To run a single test class:

```bash
mvn -Dtest=TestClassName test
```

Example:

```bash
mvn -Dtest=LoginTest test
```

---

## Run Tests from IntelliJ IDEA

1. Open the project in IntelliJ IDEA
2. Allow Maven dependencies to load
3. Navigate to:
    - `src/test/java`
4. Select the desired test class
5. Right-click the class
6. Click:
    - `Run 'TestName'`

---

# 🛠️ Test Configuration

The project configuration includes:
- Maven dependency management
- TestNG test execution configuration
- Browser setup and WebDriver initialization
- Utility classes for reusable functionality
- Page Object Model structure

The framework is designed to support:
- Easy test maintenance
- Reusable components
- Clean test structure
- Scalability for future test additions

---

# 📊 Comparison Criteria

Human-written and AI-assisted tests are compared using the following criteria:

## Efficiency
Evaluation of implementation speed and execution performance.

## Stability
Analysis of test reliability and consistency during execution.

## Maintainability
Evaluation of how easily the tests can be updated and maintained.

## Accuracy
Verification that the automation tests correctly validate expected functionality.

## Code Structure & Readability
Comparison of code organization, clarity, and adherence to automation best practices.

The purpose of the comparison is to evaluate the practical impact of AI in QA automation engineering workflows.

---

# 💡 Key Focus Areas

The project specifically focuses on:
- AI-generated automation quality
- Human vs AI implementation differences
- Test maintainability
- Real-world QA automation practices
- Automation scalability
- Reusability of automation components

---

# 💠 Recommended IDE Setup

Recommended IDE:
- IntelliJ IDEA

Recommended plugins/extensions:
- TestNG Plugin
- Maven Integration
- CheckStyle
- Git Integration

---

# ❔ Additional Notes

- The repository is intended for educational and research purposes.
- The project demonstrates practical QA automation approaches used during the collaboration.
- Automation tests were implemented using both traditional and AI-assisted workflows.
- The repository structure is organized to support readability and maintainability.
- Reusable components are separated to minimize code duplication.

---

# 👥 Team

- **Tamara Stojanoska**
- **Leonida Kostova**
- **Ilina Stevanoska**

---

# 🎓 Mentors

- **Biljana Mihajlovska**
- **Savo Kostadinov**
- **Nikola Gjurkovski**
