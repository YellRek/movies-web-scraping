import urllib.parse
import requests

def get_movie_info(title):
    try:
        title_parse_to_url = urllib.parse.quote_plus(title)
        # http://www.omdbapi.com/ API para IMDB
        r = requests.get("http://www.omdbapi.com/?apikey=7b06fceb&t=" + title_parse_to_url)
        return r.json()
    except:
        return dict()