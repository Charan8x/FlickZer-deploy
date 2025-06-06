import requests

API_KEY = "e26ac9987b0896f0c15c6a3e62fc0531"  # Replace with your real TMDB API key

url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    print("Results count:", len(data.get("results", [])))
    print("Sample movie:", data["results"][0]["title"])
except Exception as e:
    print("Error:", e)
