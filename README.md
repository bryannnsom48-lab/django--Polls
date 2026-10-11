# 🗳️ Django Polls Application

A full-stack web application that allows users to view public polls, cast votes, and see real-time results. This project is built following the official Django framework documentation to practice backend web development and database management.

## 🚀 Features
*   **Public Polls:** Anyone can view active questions and current vote tallies.
*   **Voting System:** Secure interface for casting text-based votes.
*   **Admin Dashboard:** Fully configured Django admin panel to manage questions and choices easily.
*   **Responsive Design:** Accessible on both desktop and mobile web browsers.

## 🛠️ Tech Stack
*   **Backend:** Python 3, Django Framework
*   **Database:** SQLite (Default local development)
*   **Frontend:** HTML5, CSS3, Django Template Language

## 💻 How to Run This Project Locally

Follow these steps to get a local copy up and running on your machine.

### Prerequisites
Make sure you have Python and Git installed.

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd django--Polls
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv polls_venv
   # On Windows: Command Prompt;
   .\polls_venv\Scripts\activate
   # batch:
   source /polls_venv/Scripts/activate
   ```

3. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

5. Open your browser and navigate to `http://127.0.0` to see the application live!
