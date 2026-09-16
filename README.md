# JobGrids — Job Portal & Recruitment Management System

A full-stack job portal and recruitment management platform built with Django. JobGrids provides dedicated workflows for job seekers to discover vacancies and apply for roles, while offering employers tools to publish job listings, review applicant profiles, and manage hiring stages.

## Features

- **Candidate Portal**: Profile creation, resume uploads, application tracking, and real-time status updates.
- **Employer Portal**: Company profile management, job posting creation, and applicant review workflows.
- **Administrative Control**: Integrated Django Admin with Volt Bootstrap 5 theme for employer verification, job moderation, and platform metrics.
- **Search & Filtering**: Search vacancies by keyword, industry sector, geographical location, and job type (Full-time, Remote, Contract).

## Tech Stack

- **Backend**: Python 3.11+, Django 4.2+
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (default development) / PostgreSQL

## Getting Started

### Prerequisites

Ensure you have Python 3.10+ and pip installed on your system.

### Installation

1. Clone the repository:
   `ash
   git clone https://github.com/animeshthomas/JobGrids-Django.git
   cd JobGrids-Django
   `

2. Install dependencies:
   `ash
   pip install -r requirements.txt
   `

3. Run database migrations:
   `ash
   cd seekerp
   python manage.py migrate
   `

4. Start the development server:
   `ash
   python manage.py runserver
   `

5. Open your browser and navigate to http://127.0.0.1:8000.

## Default Test Credentials

### Super Admin
- **URL**: /admin/
- Created via python manage.py createsuperuser

### Sample Employer Accounts
| Company | Email | Password | Status |
| :--- | :--- | :--- | :--- |
| Google | google@gmail.com | google | Verified |
| Amazon Web Services | aws@gmail.com | aws | Verified |
| OpenAI | openai@gmail.com | Openai@123 | Verified |
| TCS | tcs@gmail.com | Tcs@1234 | Verified |

### Sample Candidate Accounts
| Name | Email | Password |
| :--- | :--- | :--- |
| Animesh Thomas | animesh@gmail.com | animesh |
| Thomas Mathew | thomas@gmail.com | Thomas@124 |

## License

This project is licensed under the MIT License.