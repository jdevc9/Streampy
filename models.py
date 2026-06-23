from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

# Association table: movies <-> categories (many-to-many)
movie_categories = db.Table('movie_categories',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(500), default='/static/img/default-avatar.png')
    plan = db.Column(db.String(20), default='free')  # free, basic, premium
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    watch_progress = db.relationship('WatchProgress', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    watchlist = db.relationship('Watchlist', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    original_title = db.Column(db.String(200))
    synopsis = db.Column(db.Text)
    year = db.Column(db.Integer)
    duration_min = db.Column(db.Integer)  # duration in minutes
    rating = db.Column(db.Float, default=0.0)  # 0-10
    poster_url = db.Column(db.String(500))
    backdrop_url = db.Column(db.String(500))
    trailer_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500))  # actual video or demo embed
    tmdb_id = db.Column(db.Integer, unique=True, nullable=True)
    director = db.Column(db.String(200))
    cast = db.Column(db.Text)  # JSON string: ["Actor 1", "Actor 2"]
    language = db.Column(db.String(50), default='pt-BR')
    content_rating = db.Column(db.String(10), default='PG-13')  # G, PG, PG-13, R, NC-17
    is_featured = db.Column(db.Boolean, default=False)
    is_series = db.Column(db.Boolean, default=False)
    total_views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    categories = db.relationship('Category', secondary=movie_categories, backref='movies', lazy='subquery')
    watch_progress = db.relationship('WatchProgress', backref='movie', lazy='dynamic', cascade='all, delete-orphan')
    watchlist_entries = db.relationship('Watchlist', backref='movie', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='movie', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def duration_formatted(self):
        if not self.duration_min:
            return 'N/A'
        h = self.duration_min // 60
        m = self.duration_min % 60
        return f'{h}h {m}m' if h else f'{m}m'

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return self.rating
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    def __repr__(self):
        return f'<Movie {self.title} ({self.year})>'


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50), default='🎬')
    color = db.Column(db.String(20), default='#e50914')

    def __repr__(self):
        return f'<Category {self.name}>'


class WatchProgress(db.Model):
    __tablename__ = 'watch_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    position_sec = db.Column(db.Integer, default=0)  # position in seconds
    completed = db.Column(db.Boolean, default=False)
    watched_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='unique_user_movie'),)

    @property
    def progress_percent(self):
        movie = Movie.query.get(self.movie_id)
        if movie and movie.duration_min:
            total_sec = movie.duration_min * 60
            return min(100, round((self.position_sec / total_sec) * 100))
        return 0


class Watchlist(db.Model):
    __tablename__ = 'watchlist'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    position = db.Column(db.Integer, default=0)

    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='unique_watchlist'),)


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='unique_review'),)
