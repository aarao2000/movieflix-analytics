import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///movieflix.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer)
    description = db.Column(db.String(500))
    ratings = db.relationship("Rating", backref="movie", lazy=True)

    @property
    def average_score(self):
        if not self.ratings:
            return None
        return round(sum(r.score for r in self.ratings) / len(self.ratings), 2)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(300))
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def index():
    movies = Movie.query.order_by(Movie.title).all()
    return render_template("index.html", movies=movies)

@app.route("/movies", methods=["POST"])
def create_movie():
    title = request.form.get("title")
    genre = request.form.get("genre")
    year = request.form.get("year")
    description = request.form.get("description")
    if title and genre:
        movie = Movie(title=title, genre=genre, year=int(year) if year else None, description=description)
        db.session.add(movie)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/ratings", methods=["POST"])
def create_rating():
    movie_id = request.form.get("movie_id")
    score = request.form.get("score")
    comment = request.form.get("comment")
    if movie_id and score:
        rating = Rating(movie_id=int(movie_id), score=int(score), comment=comment)
        db.session.add(rating)
        db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
