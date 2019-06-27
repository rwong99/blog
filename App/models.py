from App.exts import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    alias = db.Column(db.String(20))
    count = db.Column(db.Integer)
    articles = db.relationship("Article", backref="c", lazy=True)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20))
    text = db.Column(db.String(800))
    tags = db.Column(db.String(100))
    date = db.Column(db.Date)
    comment_count = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))


class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(10))