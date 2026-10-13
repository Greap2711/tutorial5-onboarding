# Employee Onboarding & Training Management System

A web-based platform to streamline employee onboarding processes, track sequential tasks, and manage departmental roadmaps.

Developed by **Group 6** for **INS3282 - Capstone Project II (Tutorial 5)**.

---

## 1. Setup & Run Instructions

### Prerequisites
- **Python 3.10+**
- **Microsoft SQL Server** with SSMS
- **ODBC Driver 17 (or 18) for SQL Server**

### Step-by-Step Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Greap2711/tutorial5-onboarding.git](https://github.com/Greap2711/tutorial5-onboarding.git)
   cd tutorial5-onboarding
Install required dependencies:

Bash
pip install flask pyodbc
Configure local environment:

Refer to .env.example for environment variables.

Verify the SERVER configuration in app.py matches your local SQL Server instance name.

Initialize database:

Run the SQL setup script to initialize onboarding_db and populate sample seed data.

Start application:

Bash
py app.py
Open browser and navigate to: http://localhost:5000

2. Team Workflow & Branch Conventions
To ensure reproducible integration and team collaboration, Group 6 follows these branching rules:

main: Protected production branch; must remain stable and runnable at all times.

feature/<feature-name>: Dedicated branches for developing isolated requirements (e.g., feature/vertical-slice-task-status).

fix/<issue-name>: Dedicated branches for bug fixes.

docs/<doc-name>: Dedicated branches for documentation and diagram updates.

3. Pull Request & Review Policy
No Direct Commits: Direct commits to main are restricted. All changes must be delivered via Pull Requests.

Traceability: Every PR must be linked to a specific requirement/task on the task board.

Peer Review: Requires at least one approval (LGTM) from a teammate before merging.

Verification Evidence: Test results, screenshots, and migration notes must be attached to the PR.