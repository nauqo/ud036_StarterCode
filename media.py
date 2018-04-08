import os
import sys


class Movie:
    """
    Attributes:
        title (str): The title of the movie.
        poster_image_url(str): URL to the movie poster to show an image
        trailer_youtube_url(str): A trailer URL from youtube.
    """

    def __init__(self, title, poster_image_url, trailer_youtube_url):
        self.title = title
        self.poster_image_url = poster_image_url
        self.trailer_youtube_url = trailer_youtube_url

    def save_movie_to_file(self, id):
        """
        Will save the movie data into the file movies.txt as:

            id;:title;:poster_url;:youtube_url\n

            where:
                id(int): Movie ID from themoviedb.
                title(str): The title of the movie.
                poster_url(str): URL to the movie poster.
                youtube_url(str): A trailer URL from youtube.
                ;:(str): Use to split the line into a list.
        """

        with open(os.path.join(sys.path[0], "movies.txt"), "a") as file:
            file.write(str(id) + ";:" + self.title + ";:" +
                       self.poster_image_url + ";:" +
                       self.trailer_youtube_url + "\n")

    @staticmethod
    def get_data_from_movie(id, data):
        with open(os.path.join(sys.path[0], "movies.txt"), "r") as file:
            if(data == "ALL"):
                return file.readlines()
            for line in file:
                res = line.split(";:")
                if(str(id) == res[0]):
                    if(data == "title"):
                        return res[1]
                    elif(data == "poster"):
                        return res[2]
                    # Need to remove the \n at the end of line
                    elif(data == "trailer"):
                        return data[3].replace("\n", "")
                    else:
                        print("Data string not valid, check it, return False")
        return False
