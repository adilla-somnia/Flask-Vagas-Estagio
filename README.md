# Partner Companies Registration System API

This API was developed to facilitate integration between administrators, companies, and students at IFPE Campus Jaboatão. It provides RESTful endpoints that enable centralized and organized management of partner companies, job postings, and student applications.

## Features

Registration and management of partner companies

Creation, listing, and removal of job vacancies linked to companies

Student registration and application submission for available vacancies

Public listing of job vacancies accessible to students

## Tech Stack

**Back-end: Python, Flask**

## Contributing to the Project
Setting up a virtual environment and installing dependencies
```bash
  python -m venv myvenv
  . myvenv/Scripts/activate # activate the virtual environment
  pip install requirements.txt
```

Saving new dependencies to requirements.txt
```bash
  pip freeze > requirements.txt # run this inside the virtual environment
```

## Project Structure
```
Flask-Vagas-Estagio/
├── estagios/
│   ├── __pycache__/
│   ├── routes/
│   │   └── __init__.py
│   ├── models.py
│   ├── rotas.py
│   └── .env          ← Environment variables file (place it here)
├── instance/
├── venv/             ← Virtual environment (create it at the project root)
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
```

## Environment Variables

To run this project, you need to define the following environment variables in your .env file:

`SQLALCHEMY_DATABASE_URI`

`SQLALCHEMY_TRACK_MODIFICATIONS`

`MAIL_SERVER`

`MAIL_PORT`

`MAIL_USERNAME`

`MAIL_PASSWORD`

`MAIL_USE_TLS`
