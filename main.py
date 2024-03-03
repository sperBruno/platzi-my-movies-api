from typing import List, Optional
from fastapi import FastAPI, Body, Path, Query, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int]
    title: str = Field(max_length=15)
    overview: str
    year: str
    rating: int
    category: str


app = FastAPI()
app.title = "Movies API"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "test@test.com" or data["password"] != "test": 
            raise HTTPException(status_code=403, detail="invalid credentials")


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

@app.post("/login", tags=["auth"])
def login_user(user: User):
    if user.email == "test@test.com" and user.password == "test":
       token = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)

@app.get("/movies", tags=["movies"], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)


@app.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            return JSONResponse(status_code=200, content=movie)
    return JSONResponse(status_code=404, content=[])


@app.get("/movies/", tags=["movies"])
def get_movie_by_category(category: str = Query(min_length=5, max_length=15)):
    movies_by_categories = list(
        filter(lambda x: x["category"] == category, movies))
    return JSONResponse(content=movies_by_categories)


@app.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(
        movie
    )
    return JSONResponse(status_code=201, content="movie created")


@app.put("/movies/{id}", tags=["movies"])
def create_movie(id: int, movie_to_update: Movie):

    for movie in movies:
        if movie["id"] == id:
            movie["title"] = movie_to_update.title
            movie["overview"] = movie_to_update.overview
            movie["year"] = movie_to_update.year
            movie["rating"] = movie_to_update.rating
            movie["category"] = movie_to_update.category
            return JSONResponse(content=movie)


@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id: int):
    movies.remove(get_movie(id))
    print(movies)
    return JSONResponse(content="movie deleted")
