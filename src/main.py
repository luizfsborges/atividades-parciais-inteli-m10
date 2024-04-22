from flask import Flask, jsonify, request, render_template, make_response
from database.database import db
from database.models import User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, set_access_cookies

app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///var/main-instance/project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "goku-vs-vegeta"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
db.init_app(app)
jwt = JWTManager(app)

# Database initialization command
import sys
if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    with app.app_context():
        db.create_all()
    print("Database created successfully")
    sys.exit(0)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    users = User.query.all()
    return_users = []
    for user in users:
        return_users.append(user.serialize())
    return jsonify(return_users)

# Other routes for CRUD operations
# ...

@app.route("/user-login", methods=["GET"])
def user_login():
    return render_template("login.html")

@app.route("/user-register", methods=["GET"])
def user_register():
    return render_template("register.html")

@app.route("/content", methods=["GET"])
@jwt_required()
def content():
    return render_template("content.html")

@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")

@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=username, password=password).first()
    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=user.id)
    response = make_response(render_template("content.html"))
    set_access_cookies(response, access_token)
    return response

if __name__ == '__main__':
    app.run(debug=True)
