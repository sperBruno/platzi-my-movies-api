from typing import Optional
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: Optional[int]
    title:str = Field(max_length=15)
    overview:str
    year:str
    rating: int
    category: str


app = FastAPI()
app.title = "Movies API"

movies = [
    {"id": 1,
     "title": "Avatar",
     "overview": "",
     "year": "2009",
     "rating": "7.8",
     "category": "Action"},
    {"id": 2,
     "title": "Avatar",
     "overview": "",
     "year": "2009",
     "rating": "7.8",
     "category": "Fiction"},
    {"id": 3,
     "title": "Avatar",
     "overview": "",
     "year": "2009",
     "rating": "7.8",
     "category": "Action"},
]


@app.get("/", tags=["Home"])
def message():
    return HTMLResponse("<h1>Hello world!</h1>")


@app.get("/movies", tags=["movies"])
def get_movies():
    return movies


@app.get("/movies/{id}", tags=["movies"])
def get_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            return movie
    return []


@app.get("/movies/", tags=["movies"])
def get_movie_by_category(category: str = Query(min_length=5, max_length=15)):
    movies_by_categories = list(
        filter(lambda x: x["category"] == category, movies))
    return movies_by_categories


@app.post("/movies", tags=["movies"])
def create_movie(movie: Movie):
    movies.append(
        movie
    )
    return "movie created"


@app.put("/movies/{id}", tags=["movies"])
def create_movie(id: int, movie_to_update: Movie):

    for movie in movies:
        if movie["id"] == id:
            movie["title"] = movie_to_update.title
            movie["overview"] = movie_to_update.overview
            movie["year"] = movie_to_update.year
            movie["rating"] = movie_to_update.rating
            movie["category"] = movie_to_update.category
            return movie


@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id: int):
    movies.remove(get_movie(id))
    print(movies)
    return "movie deleted"
