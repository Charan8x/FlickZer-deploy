import requests

API_KEY = '0a6ba63e42fd8f1e83cd80d74a1600a4'
query = "spiderman"

url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    results = data.get('results', [])
    if results:
        print(f"Found {len(results)} movies for query '{query}':")
        for movie in results[:5]:  # print top 5 results
            print(f"- {movie.get('title')} (ID: {movie.get('id')})")
    else:
        print("No movies found for this query.")
else:
    print(f"API request failed with status code: {response.status_code}")
