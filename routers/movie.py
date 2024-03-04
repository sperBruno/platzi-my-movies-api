from fastapi import APIRouter, Depends, Query
from config.database import Session
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.responses import HTMLResponse, JSONResponse
from middlewares.jwt_bearer import JWTBearer
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder


movie_router = APIRouter()


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=15)
    overview: str
    year: str
    rating: int
    category: str


@movie_router.get("/movies", tags=["movies"], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    result = Session().query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(result))


@movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(id: int):
    result = Session().query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get("/movies/", tags=["movies"])
def get_movie_by_category(category: str = Query(min_length=5, max_length=15)):
    result = Session().query(MovieModel).filter(
        MovieModel.category == category).all()
    # movies_by_categories = list(
    #     filter(lambda x: x["category"] == category, movies))
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    # movies.append(
    #     movie
    # )
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content="movie created")


@movie_router.put("/movies/{id}", tags=["movies"])
def update_movie(id: int, movie_to_update: Movie):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})

    result.title = movie_to_update.title
    result.overview = movie_to_update.overview
    result.year = movie_to_update.year
    result.rating = movie_to_update.rating
    result.category = movie_to_update.category
    db.commit()
    return JSONResponse(content=jsonable_encoder(result))


@movie_router.delete("/movies/{id}", tags=["movies"])
def delete_movie(id: int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    db.delete(result)
    db.commit()
    return JSONResponse(content="movie deleted")
