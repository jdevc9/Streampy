from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from models import db, Movie, Category, Watchlist
from sqlalchemy import or_

catalog_bp = Blueprint('catalog', __name__)


@catalog_bp.route('/')
def home():
    # Featured movie for hero banner
    featured = Movie.query.filter_by(is_featured=True).order_by(db.func.random()).first()
    if not featured:
        featured = Movie.query.order_by(Movie.rating.desc()).first()

    # Categories with movies for carousels
    categories = Category.query.all()
    
    # Continue watching (if logged in)
    continue_watching = []
    if current_user.is_authenticated:
        from models import WatchProgress
        progress = WatchProgress.query\
            .filter_by(user_id=current_user.id, completed=False)\
            .order_by(WatchProgress.watched_at.desc())\
            .limit(10).all()
        continue_watching = [(p.movie, p.progress_percent) for p in progress]

    # Trending (most views)
    trending = Movie.query.order_by(Movie.total_views.desc()).limit(20).all()
    
    # Top rated
    top_rated = Movie.query.order_by(Movie.rating.desc()).limit(20).all()
    
    # Recently added
    recent = Movie.query.order_by(Movie.created_at.desc()).limit(20).all()

    return render_template('home.html',
        featured=featured,
        categories=categories,
        trending=trending,
        top_rated=top_rated,
        recent=recent,
        continue_watching=continue_watching
    )


@catalog_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    genre = request.args.get('genre', '')
    year = request.args.get('year', '')
    sort = request.args.get('sort', 'relevance')

    movies = []
    categories = Category.query.all()

    if query or genre or year:
        q = Movie.query

        if query:
            q = q.filter(or_(
                Movie.title.ilike(f'%{query}%'),
                Movie.synopsis.ilike(f'%{query}%'),
                Movie.director.ilike(f'%{query}%'),
                Movie.cast.ilike(f'%{query}%')
            ))

        if genre:
            cat = Category.query.filter_by(slug=genre).first()
            if cat:
                q = q.filter(Movie.categories.contains(cat))

        if year:
            q = q.filter(Movie.year == int(year))

        # Sorting
        if sort == 'rating':
            q = q.order_by(Movie.rating.desc())
        elif sort == 'year':
            q = q.order_by(Movie.year.desc())
        elif sort == 'title':
            q = q.order_by(Movie.title.asc())
        else:
            q = q.order_by(Movie.total_views.desc())

        movies = q.limit(50).all()

    return render_template('search.html',
        movies=movies,
        query=query,
        genre=genre,
        year=year,
        sort=sort,
        categories=categories
    )


@catalog_bp.route('/browse')
@catalog_bp.route('/browse/<slug>')
def browse(slug=None):
    categories = Category.query.all()
    current_category = None
    movies = []

    if slug:
        current_category = Category.query.filter_by(slug=slug).first_or_404()
        movies = current_category.movies
    else:
        movies = Movie.query.order_by(Movie.rating.desc()).all()

    return render_template('browse.html',
        categories=categories,
        current_category=current_category,
        movies=movies
    )


@catalog_bp.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    
    # Related movies (same category)
    related = []
    if movie.categories:
        related = Movie.query\
            .filter(Movie.categories.any(Category.id.in_([c.id for c in movie.categories])))\
            .filter(Movie.id != movie.id)\
            .order_by(Movie.rating.desc())\
            .limit(8).all()

    # Check if in user's watchlist
    in_watchlist = False
    user_progress = None
    user_review = None
    if current_user.is_authenticated:
        from models import WatchProgress, Review
        in_watchlist = Watchlist.query.filter_by(
            user_id=current_user.id, movie_id=movie.id
        ).first() is not None
        user_progress = WatchProgress.query.filter_by(
            user_id=current_user.id, movie_id=movie.id
        ).first()
        user_review = Review.query.filter_by(
            user_id=current_user.id, movie_id=movie.id
        ).first()

    reviews = movie.reviews.order_by(db.text('created_at desc')).limit(10).all()

    return render_template('movie_detail.html',
        movie=movie,
        related=related,
        in_watchlist=in_watchlist,
        user_progress=user_progress,
        user_review=user_review,
        reviews=reviews
    )


@catalog_bp.route('/api/watchlist/toggle', methods=['POST'])
def toggle_watchlist():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Login required'}), 401
    
    movie_id = request.json.get('movie_id')
    movie = Movie.query.get_or_404(movie_id)
    
    entry = Watchlist.query.filter_by(
        user_id=current_user.id, movie_id=movie_id
    ).first()
    
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'status': 'removed', 'message': 'Removido da lista'})
    else:
        new_entry = Watchlist(user_id=current_user.id, movie_id=movie_id)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'status': 'added', 'message': 'Adicionado à lista'})


@catalog_bp.route('/help')
def help_page():
    faqs = [
        {
            'question': 'Como posso cancelar minha assinatura?',
            'answer': 'Acesse seu perfil > Configurações > Cancelar assinatura. O cancelamento é imediato e você não será cobrado no próximo ciclo.'
        },
        {
            'question': 'Quantos dispositivos posso usar?',
            'answer': 'O plano Basic permite 1 dispositivo, o Standard permite 2 e o Premium permite 4 dispositivos simultâneos.'
        },
        {
            'question': 'Os filmes têm legendas em português?',
            'answer': 'Sim! Todo o catálogo possui legendas em português brasileiro. Muitos títulos também têm dublagem em PT-BR.'
        },
        {
            'question': 'Posso baixar conteúdo para assistir offline?',
            'answer': 'O download offline está disponível nos planos Standard e Premium, nos aplicativos iOS e Android.'
        },
        {
            'question': 'A qualidade de vídeo é HD ou 4K?',
            'answer': 'O plano Basic oferece HD (720p), o Standard oferece Full HD (1080p) e o Premium oferece 4K Ultra HD + HDR.'
        },
        {
            'question': 'Como funciona o período de teste gratuito?',
            'answer': 'Novos usuários têm acesso gratuito por 30 dias. Nenhum cartão de crédito é necessário durante o período de teste.'
        },
    ]
    return render_template('help.html', faqs=faqs)
