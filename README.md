# Flask Template
A well structured end to end template of a Flask project with following features: 

- User login and authentication
- SQLite DB
- Password Encryption via hashing `[PBKDF2:SHA256]` and salting
- File serving for download

### Methods

- `GET`
- `POST` 

## Prerequisites

- Python 3.11 and up
- SQLite using SQLAlchemy
- Login and Authentication using Flask-Login
- Password Encryption using Werkzeug Security Utils

# Setup

- Clone the project files from the repository into your local device from the terminal.

  ```bash
  git clone https://github.com/SourasishBasu/Flask-template.git
  cd Flask-template
  ```

- Initialize `venv` and install necessary libraries using `pip`.

  ```bash
  python -m venv venv
  ./venv/Scripts/activate
  pip install -r requirements.txt
  ```

- Run the app. Visit http://localhost:5000/ in your preferred browser to use various routes.
  
  ```bash
  python app.py
  ```
  
