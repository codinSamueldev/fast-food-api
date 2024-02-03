from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette import status

from services.meal_services import MealMethods
from schemas.meal_pydantic_model import Food
from config.database import local_session

DB = local_session()


meals_router = APIRouter(prefix="/food", tags=["MEALS"])


@meals_router.get("/", status_code=status.HTTP_200_OK, response_model=Food)
def get_meals(): return JSONResponse(content=jsonable_encoder(MealMethods(DB).get_all_meals_available()), status_code=status.HTTP_200_OK)


@meals_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_meal(id: int): return JSONResponse(content=jsonable_encoder(MealMethods(DB).get_meal(id)), status_code=status.HTTP_200_OK)


@meals_router.post("/", status_code=201)
def add_meal(new_meal: Food):
    MealMethods(DB).add_new_meal(new_meal_data=new_meal)

    return JSONResponse(content={"message": "Se ha añadido una nueva comida!"}, status_code=201)


@meals_router.delete("/", status_code=status.HTTP_200_OK)
def delete_all():
    MealMethods(DB).delete_all_meals_stored()

    return JSONResponse(content={"message": "Todas las comidas almacenadas fueron eliminadas satisfactoriamente."}, status_code=status.HTTP_200_OK)

