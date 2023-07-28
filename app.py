from flask import Flask, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config["SECRET_KEY"] = "ohRight,secretlySshh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()



@app.route("/api/cupcakes")
def get_all_cupcakes():
    """Gets all cupcakes' data with JSON response"""
    cupcakes = [c.serialize_cupcake() for c in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_solo_cupcake(cupcake_id):
    """Gets data about a single cupcake with JSON response"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize_cupcake()

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Creates a cupcake with flavor, size, rating and image data
    from request and responds with JSON"""
    data = request.json
    flavor = data["flavor"]
    size = data["size"]
    rating = data["rating"]
    image = data["image"] or None

    new_cupcake = Cupcake(
        flavor=flavor, 
        size=size, 
        rating=rating, 
        image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize_cupcake()
    return (jsonify(cupcake=serialized), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Updates given cupcake and responds with patched-up cake in JSON"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json

    cupcake.flavor = data.get("flavor", cupcake.flavor)
    cupcake.size = data.get("size", cupcake.size)
    cupcake.rating = data.get("rating", cupcake.rating)
    cupcake.image = data.get("image", cupcake.image)

    db.session.commit()
    serialized = cupcake.serialize_cupcake()
    
    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Deletes given cupcake from database"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

@app.route("/")
def list_cupcakes():
    """Returns static HTML listing cupcakes and showing add-new form"""
    return render_template("/index.html")