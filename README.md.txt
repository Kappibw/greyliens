# Flask Hello World Application

## Overview

This project demonstrates local Flask development setup.

The goal is to allow developers to:

1. Clone the repository
2. Install dependencies
3. Run the Flask app locally
4. Verify localhost works

---


## Clone Repository

```bash
git clone <REPOSITORY_URL>
cd <PROJECT_FOLDER>
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```


## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux


## Install Flask

```bash
pip install flask
```

## Save Dependencies

```bash
pip freeze > requirements.txt
```

---

# Running the Application

```bash
python app.py
```

---

# Verification Step

Open:

http://127.0.0.1:5000

Expected output:

Hello, Flask!

---

# Daily Development Workflow

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

## Run Flask

```bash
python app.py
```

---

# Common Setup Issues

## python not found

Try:

```bash
python3 --version
```

## flask not found

Activate virtual environment first.

Then run:

```bash
pip install -r requirements.txt
```

## Port already in use

Run:

```bash
flask run --port 5001
``