from flask_sqlalchemy import SQLAlchemy

db =  SQLAlchemy()

def connect_db(app):
    """Wraps logic into a function connecting app to database"""
    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
    """Models a cupcake object"""
    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable = False)
    size = db.Column(db.Text, nullable = False)
    rating = db.Column(db.Float, nullable = False)
    image = db.Column(db.Text, nullable = False, default = 'https://tinyurl.com/demo-cupcake')

    def serialize_cupcake(self):
        """Serialize a cupcake SQLAlchemy object into a dict"""
        return {
            "id": self.id, 
            "flavor": self.flavor,
            "size": self.size, 
            "rating": self.rating,
            "image": self.image
        }

    def __repr__(self):
        """dunder method for easy reading of programming outputs"""
        return f"<Cupcake {self.id} flavor={self.flavor} size={self.size} rating={self.rating} image={self.image} >"
