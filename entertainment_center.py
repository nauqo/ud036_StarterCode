import urllib
import json
import media
import fresh_tomatoes
import os
import sys

# Using these constant variables to build correct urls

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
IMG_W300 = "/w300"


def create_popular_movie_web_site():
    """
    From a discover call to themoviedb it will return all top popular movies
    with almost all the data, except trailer url which must be called
    separately using a movie id.

    To prevent slow processing, each movie data will be saved to a local file
    so that it can prevent extra request to themoviedb.
    """

    movies = []  # An array to be filled with movies.
    try:
        # A discover call to themoviedb, fetching the top movies.
        response = get_json_from_url(DISCOVER_URL)
        for data in response["results"]:
            title = data["title"]
            poster_url = BASE_POSTER_URL+IMG_W300+data["poster_path"]

            # Try to fetch from local file first, api request takes longer time
            try:
                id = data["id"]
                on_local = media.Movie.get_data_from_movie(id, "trailer")
                if(on_local is not False):
                    trailer = on_local
                    movie = media.Movie(title, poster_url, trailer)
                else:
                    # Will use the id to fetch trailer url from themoviedb.
                    trailer = get_movie_trailer_url(id)
                    movie = media.Movie(title, poster_url, trailer)

                    # Since it is a new movie, it should be saved.
                    movie.save_movie_to_file(id)
                movies.append(movie)

            # Sometimes some movies have no trailers,
            # they will not be shown or saved.
            except IndexError:
                print("No trailer found, will not put it on the site")

    # Will use local file instead of themoviedb.
    except IOError:
        print("Please check your api key, movies from file will be used")
        file = media.Movie.get_data_from_movie(0, "ALL")
        for line in file:
            data = line.split(";:")
            title = data[1]
            poster_url = data[2]
            trailer = data[3]
            movie = media.Movie(title, poster_url, trailer)
            movies.append(movie)
    fresh_tomatoes.open_movies_page(movies)


def get_movie_trailer_url(id):
    # themoviedb api doesn't give movie trailers(using discover),
    # so a call using the movie id is needed to get youtube key
    movie_url = BASE_URL + MOVIE + str(id) + API + API_KEY + APPEND_VIDEOS
    data = get_json_from_url(movie_url)

    # Get the first trailer key
    youtube_key = data["videos"]["results"][0]["key"]
    trailer_url = YOUTUBE_URL + youtube_key
    return trailer_url


def get_json_from_url(url):
    # Fetch json obj from url
    response = urllib.urlopen(url)

    # Save it into data and returns the data
    data = json.loads(response.read())
    response.close()
    return data

create_popular_movie_web_site()
