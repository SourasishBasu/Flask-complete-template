from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

login_manager = LoginManager() # Initializing Login Manager to secure site
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.config['UPLOAD_FOLDER'] = './static/files'
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CREATE TABLE IN DB
class User(UserMixin, db.Model): # UserMixin used for Flask-Login and checking for logged in user sessions
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

# Line below only required once, when creating DB.
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


# Add new user details and salt the password before storing it
@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        exists = User.query.filter_by(email=request.form["email"]).first()
        if not exists:
            password = generate_password_hash(request.form["password"], method='pbkdf2:sha256', salt_length=8)
            new_user = User(email=request.form["email"], password=password,
                            name=request.form["name"])
            db.session.add(new_user)
            db.session.commit()
            print("Added new user successfully")

            login_user(new_user) # Login the user and redirect them to the download page

            return render_template("secrets.html", name=request.form["name"])
        else:
            flash('Email already exists!')
            return redirect(url_for('login'))

    return render_template("register.html")


# Query the DB by email to check whether valid password entered by user against its salted hashed in the DB
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        existing_user = User.query.filter_by(email=request.form["email"]).first() # Extracting user record if it exists

        if existing_user:
            if check_password_hash(pwhash=existing_user.password, password=request.form["password"]):
                login_user(existing_user)  # Login if valid pass

                return redirect(url_for('secrets', name=existing_user.name))  # Redirect to file download page
            else:
                flash("Incorrect password. Please try again.")
                return redirect(url_for('login'))
        else:
            flash("Email doesn't exist, please try again.")
            return redirect(url_for('login'))
    return render_template("login.html")


# Route for the download link of the file
@app.route('/secrets')
@login_required
def secrets():
    # name = current_user.name // From Flask-Login
    name = request.args.get('name')
    print(f"{name} logged in")  # Pass the name of the current user to the html
    return render_template("secrets.html", name=name)


# Logout currently logged-in user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# Serve file for download from local directory
@app.route('/download')
@login_required
def download():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'cheat_sheet.pdf', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
