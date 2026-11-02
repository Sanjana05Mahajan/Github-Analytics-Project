# GitHub Repository Analytics Dashboard

## Project Overview
The GitHub Repository Analytics Dashboard is a Python Flask web application that retrieves public GitHub repository information using the GitHub REST API. It displays repository statistics, calculates a custom health score, stores search history in MySQL, and compares repositories.

## Features
- Search public GitHub repositories.
- Display stars, forks, open issues, language, and other repository details.
- Calculate a repository health score and status.
- Store repository search history in MySQL.
- Compare two GitHub repositories.
- Provide REST API endpoints that return JSON.
- Handle invalid inputs, missing repositories, network errors, and API rate limits.

## Technologies Used
- Python
- Flask
- GitHub REST API
- MySQL
- HTML and CSS
- Requests
- JSON

## Project Structure
```text
github_analytics_dashboard/
├── app.py
├── github_api.py
├── analytics.py
├── database.py
├── config.py
├── requirements.txt
├── templates/
├── static/
└── README.md
```

## Setup Instructions

1. Clone or download this repository.
2. Open the project folder in VS Code.
3. Install the required packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create a MySQL database named `github_analytics`.
5. Configure the MySQL connection details in `config.py` or the environment variables used by your application.
6. Start the application:

   ```bash
   python app.py
   ```

7. Open `http://127.0.0.1:5000` in your browser.

## REST API Endpoints

### Repository Details
`GET /api/repository/<owner>/<repo>`

Returns repository details as JSON.

Example:
`/api/repository/pallets/flask`

### Repository Metrics
`GET /api/repository/<owner>/<repo>/metrics`

Returns repository metrics, health score, and status.

Example:
`/api/repository/pallets/flask/metrics`

## Error Handling
The application validates user inputs and handles missing repositories, connection failures, timeouts, and GitHub API rate limits.

## Future Improvements
- Add charts for repository statistics.
- Improve health score calculations.
- Add automated tests.
- Deploy the application to a cloud platform.

## Author
Sanjana Mahajan
