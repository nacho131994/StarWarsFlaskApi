"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory, abort, redirect
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_extended import create_access_token, current_user, jwt_required, JWTManager
from api.utils import APIException, generate_sitemap
from api.models import Favorite, User, Person, Planet, db
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands

ENV = os.getenv("FLASK_ENV")
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')
app = Flask(__name__)
app.url_map.strict_slashes = False

app.config["JWT_SECRET_KEY"] = "ceci y coco"

# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type = True)
db.init_app(app)

#  JWTManager init
jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


# Allow CORS requests to this API
CORS(app)

# add the admin
setup_admin(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route("/login", methods=["POST"])
def login():
    email = request.get_json(force=True).get("email", None)
    password = request.get_json(force=True).get("password", None)

    user = User.query.filter_by(email=email).one_or_none()
    if not user or not user.check_password(password):
        return jsonify("Wrong email or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


@app.route("/who_am_i", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(
        id=current_user.id,
        email=current_user.email
    )


@app.route('/favorites/<target>', methods=["GET"])
@jwt_required()
def get_favorites(target):
    favs = Favorite.query.filter_by(user_id=current_user.id, target=target)
    return jsonify({target: [f.target_id for f in favs]}), 200
    


@app.route('/favorites/<target>/<int:id>', methods=["POST"])
@jwt_required()
def add_favorites(target, id):
    fav = Favorite()
    fav.user_id = current_user.id
    fav.target = target
    fav.target_id = id
    fav.save()
    return jsonify(
        {"status": "added", "email": current_user.email, "target": target, "target_id": id}
    ), 200


@app.route('/favorites/<target>/<int:id>', methods=["DELETE"])
@jwt_required()
def delete_favorites(target, id):
    Favorite.query.filter_by(user_id=current_user.id, target=target, target_id=id).delete()
    db.session.commit()
    return jsonify(
        {"status": "deleted", "email": current_user.email, "target": target, "target_id": id}
    ), 200


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')


@app.route('/people', methods=['GET'])
def handle_people():
    people = Person.query.all()
    return jsonify([p.serialize() for p in people])


@app.route('/people/<int:id>', methods=['GET'])
def get_person(id):
    person = Person.query.get(id)
    return jsonify(person.serialize())


@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets])


@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planet.query.get(id)
    return jsonify(planet.serialize())


# any other endpoint will try to serve it like a static file
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0 # avoid cache memory
    return response


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)