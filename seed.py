"""
seed.py — Popula o banco com dados de exemplo.
Execute: python seed.py

Opção com TMDB API real:
  Defina TMDB_API_KEY no arquivo .env para buscar dados reais.
  Sem API key, usa dados de exemplo estáticos.
"""

import sys
import os
import requests

sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from models import db, User, Movie, Category, movie_categories

app = create_app('development')


CATEGORIES = [
    {'name': 'Ação', 'slug': 'acao', 'icon': '💥', 'color': '#dc2626', 'description': 'Filmes cheios de adrenalina e aventura'},
    {'name': 'Drama', 'slug': 'drama', 'icon': '🎭', 'color': '#7c3aed', 'description': 'Histórias que tocam o coração'},
    {'name': 'Comédia', 'slug': 'comedia', 'icon': '😂', 'color': '#d97706', 'description': 'Para rir muito'},
    {'name': 'Terror', 'slug': 'terror', 'icon': '👻', 'color': '#1e293b', 'description': 'Filmes de arrepiar'},
    {'name': 'Ficção Científica', 'slug': 'ficcao-cientifica', 'icon': '🚀', 'color': '#0891b2', 'description': 'O futuro começa aqui'},
    {'name': 'Romance', 'slug': 'romance', 'icon': '❤️', 'color': '#db2777', 'description': 'Histórias de amor inesquecíveis'},
    {'name': 'Documentário', 'slug': 'documentario', 'icon': '🎥', 'color': '#16a34a', 'description': 'A realidade em suas múltiplas formas'},
    {'name': 'Animação', 'slug': 'animacao', 'icon': '🎨', 'color': '#7c3aed', 'description': 'Para todas as idades'},
]

# Sample movies — uses public demo video and TMDB poster URLs
SAMPLE_MOVIES = [
    {
        'title': 'O Cavaleiro das Trevas', 'year': 2008, 'rating': 9.0,
        'duration_min': 152, 'content_rating': '12+', 'director': 'Christopher Nolan',
        'cast': 'Christian Bale, Heath Ledger, Aaron Eckhart',
        'synopsis': 'Batman eleva a guerra ao crime de Gotham a novos patamares, mas um criminoso que semeia o caos, conhecido como Coringa, ameaça devastar tudo.',
        'poster_url': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg',
        'backdrop_url': 'https://image.tmdb.org/t/p/original/nMKdUUepR0i5zn0y1T4CejMntit.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=EXeTwQWrcwY',
        'video_url': 'https://www.youtube.com/watch?v=EXeTwQWrcwY',  # Add real video URL here
        'categories': ['acao', 'drama'],
        'is_featured': True,
        'total_views': 45230,
    },
    {
        'title': 'Interestelar', 'year': 2014, 'rating': 8.7,
        'duration_min': 169, 'content_rating': '12+', 'director': 'Christopher Nolan',
        'cast': 'Matthew McConaughey, Anne Hathaway, Jessica Chastain',
        'synopsis': 'Um grupo de exploradores usa um buraco de minhoca recém-descoberto para superar as limitações das viagens espaciais humanas.',
        'poster_url': 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
        'backdrop_url': 'https://image.tmdb.org/t/p/original/xJHokMbljvjADYdit5fK5VQsXEG.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=zSWdZVtXT7E',
        'video_url': 'https://www.youtube.com/watch?v=zSWdZVtXT7E',
        'categories': ['ficcao-cientifica', 'drama'],
        'is_featured': True,
        'total_views': 38900,
    },
    {
        'title': 'Pulp Fiction: Tempo de Violência', 'year': 1994, 'rating': 8.9,
        'duration_min': 154, 'content_rating': '18+', 'director': 'Quentin Tarantino',
        'cast': 'John Travolta, Uma Thurman, Samuel L. Jackson',
        'synopsis': 'As vidas de dois assassinos da máfia, um boxeador, um gângster e sua esposa se entrelaçam em quatro histórias de violência e redenção.',
        'poster_url': 'https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg',
        'backdrop_url': 'https://image.tmdb.org/t/p/original/suaEOtk1N1sgg2MTM7oZd2cfVp3.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=s7EdQ4FqbhY',
        'video_url': 'https://www.youtube.com/watch?v=s7EdQ4FqbhY',
        'categories': ['acao', 'comedia'],
        'is_featured': False,
        'total_views': 29400,
    },
    {
        'title': 'Forrest Gump: O Contador de Histórias', 'year': 1994, 'rating': 8.8,
        'duration_min': 142, 'content_rating': 'L',
        'director': 'Robert Zemeckis',
        'cast': 'Tom Hanks, Robin Wright, Gary Sinise',
        'synopsis': 'A presidência de Kennedy e Johnson, o Vietnã, o escândalo Watergate e outras histórias se desdobram através da perspectiva de um homem do Alabama com QI 75.',
        'poster_url': 'https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg',
        'backdrop_url': 'https://image.tmdb.org/t/p/original/ghgfzbEV7kbpbi1O8OfTSFy9OJ6.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=uPIEn0M8su0',
        'video_url': 'https://www.youtube.com/watch?v=uPIEn0M8su0',
        'categories': ['drama', 'romance'],
        'is_featured': False,
        'total_views': 33100,
    },
    {
        'title': 'Matrix', 'year': 1999, 'rating': 8.7,
        'duration_min': 136, 'content_rating': '14+',
        'director': 'Lana e Lilly Wachowski',
        'cast': 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss',
        'synopsis': 'Um programador descobre que a realidade como conhecemos é uma simulação criada por máquinas para subjugar a humanidade.',
        'poster_url': 'https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg',
        'backdrop_url': 'https://image.tmdb.org/t/p/original/fNG7i7RqMErkcqhohV2a6cV1Ehy.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=vKQi3bBA1y8',
        'video_url': 'https://www.youtube.com/watch?v=vKQi3bBA1y8',
        'categories': ['acao', 'ficcao-cientifica'],
        'is_featured': False,
        'total_views': 27800,
    },
    {
        'title': 'O Senhor dos Anéis: A Sociedade do Anel', 'year': 2001, 'rating': 8.9,
        'duration_min': 228, 'content_rating': '12+',
        'director': 'Peter Jackson',
        'cast': 'Elijah Wood, Ian McKellen, Orlando Bloom',
        'synopsis': 'Um jovem hobbit herda um anel mágico que contém o poder de destruir a Terra-Média e parte em uma perigosa jornada para destruí-lo.',
        'poster_url': 'https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg',
        'backdrop_url': 'https://image.tmdb.org/t/p/original/pIgHoRSLtFqME0AEbPaxgmI6R43.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=V75dMMIW2B4',
        'video_url': 'https://www.youtube.com/watch?v=V75dMMIW2B4',
        'categories': ['acao', 'drama'],
        'is_featured': False,
        'total_views': 41000,
    },
    {
        'title': 'Parasita', 'year': 2019, 'rating': 8.5,
        'duration_min': 132, 'content_rating': '14+',
        'director': 'Bong Joon-ho',
        'cast': 'Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong',
        'synopsis': 'Toda a família desempregada Ki-taek começa a se infiltrar na rica família Park — uma sátira social afiada sobre desigualdade de classes.',
        'poster_url': 'https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg',
        'backdrop_url': 'https://image.tmdb.org/t/p/original/TU9NIjwzjoKPwQHoHshkFcQUCG.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=5xH0HfJHsaY',
        'video_url': 'https://www.youtube.com/watch?v=5xH0HfJHsaY',
        'categories': ['drama', 'terror'],
        'is_featured': True,
        'total_views': 22500,
    },
    {
        'title': 'Coco', 'year': 2017, 'rating': 8.4,
        'duration_min': 105, 'content_rating': 'L',
        'director': 'Lee Unkrich, Adrian Molina',
        'cast': 'Anthony Gonzalez, Gael García Bernal, Benjamin Bratt',
        'synopsis': 'Aspirante a músico Miguel é transportado para a Terra dos Mortos na noite do Dia dos Mortos, onde encontra a ajuda de um bumbuneiro improvável.',
        'poster_url': 'https://image.tmdb.org/t/p/w500/gGEsBPAijhVUFoiNpgZXqRVWJt2.jpg',
        'backdrop_url': 'https://image.tmdb.org/t/p/original/askg3SMvhqEl4OL52YuvdtY40Yb.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=Ga6RYejo6Hk',
        'video_url': 'https://www.youtube.com/watch?v=Ga6RYejo6Hk',
        'categories': ['animacao', 'drama'],
        'is_featured': False,
        'total_views': 18700,
    },
]


def seed():
    with app.app_context():
        print("🌱 Iniciando seed do banco de dados...")

        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create categories
        cat_map = {}
        for cat_data in CATEGORIES:
            cat = Category(**cat_data)
            db.session.add(cat)
            cat_map[cat_data['slug']] = cat
        db.session.flush()
        print(f"✅ {len(CATEGORIES)} categorias criadas")

        # Create movies
        for m_data in SAMPLE_MOVIES:
            cat_slugs = m_data.pop('categories')
            movie = Movie(**m_data)
            for slug in cat_slugs:
                if slug in cat_map:
                    movie.categories.append(cat_map[slug])
            db.session.add(movie)

        db.session.flush()
        print(f"✅ {len(SAMPLE_MOVIES)} filmes criados")

        # Create admin/demo user
        admin = User(username='admin', email='admin@streampy.com', plan='premium')
        admin.set_password('admin123')
        db.session.add(admin)

        demo = User(username='demo', email='demo@streampy.com', plan='basic')
        demo.set_password('demo123')
        db.session.add(demo)

        db.session.commit()
        print("✅ Usuários demo criados: admin@streampy.com / admin123")
        print("\n🎉 Seed concluído! Execute: python app.py")


if __name__ == '__main__':
    seed()
