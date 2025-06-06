from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

API_KEY = "Your_actual_TMDB_api_key"
BASE_URL = "https://api.themoviedb.org/3"

# Cache to store movie_id -> imdb_id mapping
imdb_cache = {}

def get_tmdb_data(endpoint, params=None):
    if params is None:
        params = {}
    params["api_key"] = API_KEY
    url = BASE_URL + endpoint
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching TMDB data for {url}: {e}")
        return None

def get_imdb_url(movie_id):
    if movie_id in imdb_cache:
        imdb_id = imdb_cache[movie_id]
    else:
        data = get_tmdb_data(f"/movie/{movie_id}/external_ids")
        imdb_id = data.get("imdb_id") if data else None
        imdb_cache[movie_id] = imdb_id

    return f"https://www.imdb.com/title/{imdb_id}" if imdb_id else "#"

@app.route("/")
def home():
    genre_name = request.args.get("genre")
    genre_id = None

    if genre_name:
        genre_id = GENRE_NAME_TO_ID.get(genre_name.lower())

    if genre_id:
        movies_data = get_tmdb_data("/discover/movie", params={"with_genres": genre_id, "sort_by": "popularity.desc"})
    else:
        movies_data = get_tmdb_data("/movie/popular")

    if movies_data and "results" in movies_data:
        movies = movies_data["results"]
        random.shuffle(movies)
    else:
        movies = []

    trending = movies[:8]

    # Pre-fetch IMDb URLs
    imdb_urls = {movie["id"]: get_imdb_url(movie["id"]) for movie in movies}

    return render_template("index.html", popular=movies, trending=trending, get_imdb_url=get_imdb_url, genres=GENRE_ID_TO_NAME, imdb_urls=imdb_urls)

@app.route("/search")
def search():
    query = request.args.get("query")
    search_data = get_tmdb_data("/search/movie", params={"query": query})
    results = search_data.get("results", []) if search_data else []

    imdb_urls = {movie["id"]: get_imdb_url(movie["id"]) for movie in results}

    return render_template("index.html", popular=results, trending=[], get_imdb_url=get_imdb_url, genres=GENRE_ID_TO_NAME, imdb_urls=imdb_urls)

# Genre mappings
GENRE_ID_TO_NAME = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western",
}

# Reverse mapping to get ID from name
GENRE_NAME_TO_ID = {name.lower(): id for id, name in GENRE_ID_TO_NAME.items()}

if __name__ == "__main__":
    app.run(debug=True)
