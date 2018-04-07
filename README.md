# Movie Trailer Website project
This is the first project for the Full stack web developer nanodegree program
at [udacity](https://udacity.com/).

The project is to make a web site using python. The web site will display several movie poster, when clicked it will display the trailer.

This project uses [themoviedb](https://www.themoviedb.org/) api. It will however work without an api key, but then it will not display the latest top movies.

## Getting Started
First you will need an api key from [themoviedb](https://www.themoviedb.org/).

Then simply put it in the `API_KEY` variable in **entertainment_center.py** file.
```
API_KEY=""
```
Without an api key the program will only use the local cached file.

To start the program you only need to run the **entertainment_center.py** file.

## Known issues
It is really slow because how themoviedb works. Using their discovery to fetch top movies does not include trailer information. Therefor a separate call to each movie need to be done, which is why it is very slow. The work around is by using a local file to save movie information it could get the movie information much faster.
