# JobPortal — Django

A full conversion of the React JobPortal front-end into a Django project.

## Project Structure

```
job_portal_django/
├── job_portal_django/      # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── portal/                 # Main app
│   ├── models.py           # User, Job, Application, SavedJob
│   ├── views.py            # All page views
│   ├── forms.py            # Login, Signup, PostJob, Application forms
│   ├── urls.py             # URL routing
│   ├── admin.py            # Django admin registration
│   ├── seed.py             # Demo data seeder
│   ├── templates/portal/   # Django HTML templates
│   │   ├── base.html
│   │   ├── job_listings.html
│   │   ├── job_detail.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── post_job.html
│   │   ├── applications.html
│   │   └── dashboard.html
│   └── static/portal/
│       ├── css/styles.css
│       └── js/app.js
├── manage.py
└── requirements.txt
```

## Setup & Run

```bash
# 1. Install Django
pip install -r requirements.txt

# 2. Run migrations (creates SQLite database)
python manage.py migrate

# 3. Seed demo data (users + sample jobs)
python manage.py shell < portal/seed.py

# 4. Start the dev server
python manage.py runserver
```

Then open http://127.0.0.1:8000/

## Demo Credentials

| Role     | Email                 | Password |
|----------|-----------------------|----------|
| Job Seeker | user@example.com    | password |
| Employer   | admin@example.com   | admin    |

## Pages & URLs

| URL                        | Page               | Access       |
|----------------------------|--------------------|--------------|
| `/`                        | Job Listings       | Public       |
| `/jobs/<id>/`              | Job Detail + Apply | Public       |
| `/login/`                  | Sign In            | Public       |
| `/signup/`                 | Create Account     | Public       |
| `/dashboard/`              | User Dashboard     | Job Seekers  |
| `/post-job/`               | Post a Job         | Employers    |
| `/applications/`           | View Applications  | Employers    |

## Features

- **Job Listings** — search by keyword, filter by type (Full-time, Part-time, Contract, Freelance)
- **Job Detail** — full description, requirements, apply form, save/unsave job
- **Auth** — login, signup with role selection (Job Seeker / Employer)
- **Dashboard** — (Job Seekers) stats, recent applications, saved jobs
- **Post a Job** — (Employers) form to create new listings
- **Applications** — (Employers) review & update application statuses
- **Django Admin** — manage all data at `/admin/`
