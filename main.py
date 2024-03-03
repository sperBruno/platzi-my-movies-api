from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse


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
def get_movie_by_category(category: str):
    movies_by_categories = list(
        filter(lambda x: x["category"] == category, movies))
    return movies_by_categories


@app.post("/movies", tags=["movies"])
def create_movie(id: int = Body(), title: str = Body(),
                 overview: str = Body(), rating: str = Body(), year: int = Body(), category: str = Body()):
    movies.append(
        {"id": id,
         "title": title,
         "overview": overview,
         "year": year,
         "rating": rating,
         "category": category}
    )
    return "movie created"


@app.put("/movies/{id}", tags=["movies"])
def create_movie(id: int, title: str = Body(),
                 overview: str = Body(), rating: str = Body(), year: int = Body(), category: str = Body()):

    for movie in movies:
        if movie["id"] == id:
            movie["title"] = title
            movie["overview"] = overview
            movie["year"] = year
            movie["rating"] = rating,
            movie["category"] = category
            return movie


@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id: int):
    movies.remove(get_movie(id))
    print(movies)
    return "movie deleted"
