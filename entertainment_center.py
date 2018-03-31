import urllib, json, media, fresh_tomatoes, os,sys

# I am using these constant variables to build correct urls

# Put your api key below
API_KEY = ""

# Base urls
BASE_URL = "https://api.themoviedb.org/3"
BASE_POSTER_URL = "https://image.tmdb.org/t/p"
YOUTUBE_URL = "https://www.youtube.com/watch?v="

# Required in movie_url
API = "?api_key="

# Optional
APPEND_VIDEOS = "&append_to_response=videos"
LANG_ENG = "&language=en-US"
SORT_POPULAR = "&sort_by=popularity.desc"

# Api get url methods
DISCOVER = "/discover/movie?api_key="
MOVIE = "/movie/"

# Constant url
DISCOVER_URL = BASE_URL+DISCOVER+API_KEY+LANG_ENG+SORT_POPULAR

# Size of the displayed image
IMG_W300 = "/w300";

def create_popular_movie_web_site():
    # An array to be filled with movies
    movies = []

    # A discover call to themoviedb, fetching the top movies
    data = get_json_from_url(DISCOVER_URL)
    for result in data["results"]:
        title = result["title"]
        poster_url = BASE_POSTER_URL+IMG_W300+result["poster_path"]

        # Sometimes some movies have no trailers, they will not be shown.
        try:
            trailer = get_movie_trailer_url(result["id"])
            movie = media.Movie(title,poster_url,trailer)
            movies.append(movie)
        except IndexError:
            print("No trailer found, will not put it on the site")
    fresh_tomatoes.open_movies_page(movies)


def get_movie_trailer_url(movie_id):

    on_local = get_trailer_local(movie_id)
    if(on_local != False):
        return on_local
    else :
        # themoviedb api doesn't give movie trailers(using discover),
        # so a call using the movie id is needed to get youtube key
        movie_url = BASE_URL+MOVIE+str(movie_id)+API+API_KEY+APPEND_VIDEOS
        data = get_json_from_url(movie_url)

        # Get the first trailer key
        youtube_key = data["videos"]["results"][0]["key"]
        trailer_url = YOUTUBE_URL+youtube_key

        save_trailer(movie_id, trailer_url)
        return trailer_url

def get_json_from_url(url):
    # Fetch json obj from url
    response = urllib.urlopen(url)

    # Save it into data and returns the data
    data = json.loads(response.read())
    response.close()
    return data


def get_trailer_local(id):
    with open(os.path.join(sys.path[0], "youtube_trailer_url.txt"),"r") as file:
        # Splitting up the string from line to a list, so that the
        # ID can be checked and the url can be extracted
        for line in file:
            data = line.split(" ")
            if(id == int(data[0])):
                # Removes \n at the end of the string
                result = data[1].replace("\n","")
                return result
    return False

def save_trailer(id,youtube_url):
    with open(os.path.join(sys.path[0], "youtube_trailer_url.txt"),"a") as file:
        file.write(str(id)+" "+youtube_url+"\n")

create_popular_movie_web_site()
