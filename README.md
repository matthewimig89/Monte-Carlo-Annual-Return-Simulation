# Monte Carlo Annual Return Simulation Web App

## Overview

This project is a Flask web application that performs Monte Carlo simulations to analyze investment outcomes. It uses historical annual returns of the S&P 500 (^GSPC) from Yahoo Finance to simulate potential future investment scenarios. The application allows users to input parameters such as:

*   **Number of Years:** The investment time horizon.
*   **Number of Simulations:** How many Monte Carlo simulations to run.
*   **Initial Investment:** The starting investment amount.
*   **Withdrawal Rate:** The annual percentage to withdraw from the portfolio each year.

After running the simulation, the application displays:

*   **Deciles of Ending Asset Values:** A table showing the 10th, 20th, 30th, ..., 90th percentile ending asset values after the simulation period, taking into account annual withdrawals.
*   **Average Cumulative Return:** The average overall return across all simulations.
*   **Average Annualized Return:** The approximate average annual return (calculated before withdrawals are considered in the annualized return).

This tool is designed to help visualize the range of potential investment outcomes and understand the impact of withdrawal rates on portfolio longevity using Monte Carlo simulation techniques and historical market data.

## Prerequisites

Before you can run this application, you need to have Python installed on your system, along with `pip` (Python's package installer). You also need to have the project files, including:

*   `app.py` (the main Flask application file)
*   `templates` folder containing `index.html` (the HTML template for the web page)
*   (Optionally, a `requirements.txt` file - see setup instructions)

## Setup and Run Locally (Development)

Follow these steps to set up and run the application on your local machine for development purposes:

1.  **Navigate to the Project Directory:**
    Open your command prompt or terminal and navigate to the directory where you have saved the project files (`app.py`, `templates` folder, etc.). For example, if your project is in `C:\Users\YourUsername\Documents\GitHub\Monte-Carlo-Annual-Return-Simulation`, use the `cd` command:

    ```bash
    cd C:\Users\YourUsername\Documents\GitHub\Monte-Carlo-Annual-Return-Simulation
    ```

2.  **Create a Virtual Environment (Recommended):**
    It's best practice to create a virtual environment to isolate project dependencies.  Run this command:

    ```bash
    python -m venv venv
    ```

    This will create a folder named `venv` in your project directory.

3.  **Activate the Virtual Environment:**
    Activate the virtual environment. The command differs based on your operating system:

    *   **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

    (After activation, you should see `(venv)` at the beginning of your command prompt line.)

4.  **Install Python Dependencies:**
    Install the required Python packages using `pip`. It's recommended to have a `requirements.txt` file in your project directory. If you don't have one yet, you can create it by running `pip freeze > requirements.txt` after installing the packages manually the first time.  To install from `requirements.txt` (if you have it):

    ```bash
    pip install -r requirements.txt
    ```

    If you don't have `requirements.txt` yet, or want to install manually, use:

    ```bash
    pip install Flask yfinance pandas numpy
    ```

5.  **Run the Flask Application:**
    Execute the `app.py` file to start the Flask development server:

    ```bash
    python app.py
    ```

    You should see output in your terminal indicating that the Flask app is running, usually on `http://127.0.0.1:5000`.

6.  **Access the Application in Your Browser:**
    Open your web browser and go to the address provided in the terminal (typically `http://127.0.0.1:5000/`). You should see the Monte Carlo Simulation web interface.

7.  **Stop the Development Server:**
    To stop the Flask development server, press `Ctrl+C` in the terminal where it is running.

## How to Use the Application

1.  **Open the web application in your browser** as described in the "Setup and Run Locally" section.

2.  **Input Simulation Parameters:**
    On the webpage, you will see input fields for:
    *   **Number of Years:** Enter the number of years you want to simulate your investment over.
    *   **Number of Simulations:**  Enter the number of Monte Carlo simulations you want to run (more simulations provide a more robust analysis but take longer to compute).
    *   **Initial Investment:** Enter the initial amount of money you are investing.
    *   **Withdrawal Rate (%):** Enter the annual withdrawal rate as a percentage (e.g., enter `4` for a 4% withdrawal rate).

3.  **Run Simulation:**
    Click the "Run Simulation" button.

4.  **View Results:**
    After the simulation completes (this might take a few seconds depending on the number of simulations), the page will update to display:
    *   **Decile Distribution of Ending Asset Values:** A table showing the 10th through 90th percentile values for the portfolio value at the end of the simulation period, after annual withdrawals.
    *   **Average Cumulative Return:** The average total return across all simulations.
    *   **Average Annualized Return:**  The average yearly return rate (before considering withdrawals in the annualized calculation).

## Deployment (Making it Publicly Accessible)

To make this web application accessible to others on the internet, you need to deploy it to a web hosting service. Some beginner-friendly options include:

*   **PythonAnywhere:**  Easy to use, designed for Python apps, free tier available.
*   **Render:**  Simple deployment, integrates with GitHub, free tier available.
*   **Heroku:**  Historically popular, but now requires a paid plan for new projects.

For deployment, you will generally need to:

1.  **Choose a Hosting Platform:** Sign up for an account on a hosting platform like PythonAnywhere or Render.
2.  **Prepare for Deployment:**
    *   **`requirements.txt`:**  Make sure you have a `requirements.txt` file in your project root (create it using `pip freeze > requirements.txt` if you haven't already).
    *   **`Procfile` (Potentially):** Some platforms (like Heroku, and sometimes Render) require a `Procfile` to specify how to start your application. Create a file named `Procfile` (no extension) with the content: `web: gunicorn app:app`

3.  **Follow the Hosting Platform's Deployment Instructions:** Each platform has its own specific steps. Refer to their documentation for deploying Flask applications.  This usually involves uploading your project files, setting up a Python environment, and configuring the web server.

## Dependencies

This project relies on the following Python libraries, which are listed in `requirements.txt`:

*   `Flask`
*   `yfinance`
*   `pandas`
*   `numpy`

These are installed using `pip install -r requirements.txt` (or `pip install ...` individually).

---

This README provides a comprehensive guide to understanding, setting up, running, and deploying your Monte Carlo Annual Return Simulation web application. Good luck!
