from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models import db, Movie, WatchProgress, Review

player_bp = Blueprint('player', __name__)


@player_bp.route('/watch/<int:movie_id>')
@login_required
def watch(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    
    # Increment view counter
    movie.total_views += 1
    
    # Get or create watch progress
    progress = WatchProgress.query.filter_by(
        user_id=current_user.id,
        movie_id=movie.id
    ).first()
    
    if not progress:
        progress = WatchProgress(user_id=current_user.id, movie_id=movie.id)
        db.session.add(progress)
    
    db.session.commit()

    # Related movies
    related = []
    if movie.categories:
        from models import Category
        related = Movie.query\
            .filter(Movie.categories.any(Category.id.in_([c.id for c in movie.categories])))\
            .filter(Movie.id != movie.id)\
            .order_by(Movie.rating.desc())\
            .limit(6).all()

    return render_template('player.html',
        movie=movie,
        progress=progress,
        related=related
    )


@player_bp.route('/api/progress', methods=['POST'])
@login_required
def update_progress():
    """Called by the video player every 30 seconds to save position."""
    data = request.json
    movie_id = data.get('movie_id')
    position_sec = data.get('position_sec', 0)
    completed = data.get('completed', False)

    progress = WatchProgress.query.filter_by(
        user_id=current_user.id,
        movie_id=movie_id
    ).first()

    if not progress:
        progress = WatchProgress(
            user_id=current_user.id,
            movie_id=movie_id
        )
        db.session.add(progress)

    progress.position_sec = int(position_sec)
    progress.completed = completed
    db.session.commit()

    return jsonify({'status': 'ok', 'position': progress.position_sec})


@player_bp.route('/api/review', methods=['POST'])
@login_required
def submit_review():
    data = request.json
    movie_id = data.get('movie_id')
    rating = data.get('rating')
    comment = data.get('comment', '').strip()

    if not (1 <= int(rating) <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400

    review = Review.query.filter_by(
        user_id=current_user.id,
        movie_id=movie_id
    ).first()

    if review:
        review.rating = int(rating)
        review.comment = comment
    else:
        review = Review(
            user_id=current_user.id,
            movie_id=movie_id,
            rating=int(rating),
            comment=comment
        )
        db.session.add(review)

    db.session.commit()
    return jsonify({'status': 'ok', 'message': 'Avaliação salva!'})
