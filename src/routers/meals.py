from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette import status
from typing import Annotated

from services.meal_services import MealMethods
from schemas.meal_pydantic_model import Food
from config.database import local_session
from .security.jwt_security_flow import oauth2_bearer

DB = local_session()


meals_router = APIRouter(prefix="/food", tags=["MEALS"])


@meals_router.get("/", status_code=status.HTTP_200_OK, response_model=Food, description="Obten todos los alimentos disponibles almacenados en la base de datos; si no hay alimentos almacenados retornará un error.")
def get_meals(token: Annotated[str, Depends(oauth2_bearer)]): return JSONResponse(content=jsonable_encoder(MealMethods(DB).get_all_meals_available()), status_code=status.HTTP_200_OK)


@meals_router.get("/{id}", status_code=status.HTTP_200_OK, description="Obten un alimento almacenado en la base de datos; si no se encuentra retornará un error.")
def get_meal(id: int): return JSONResponse(content=jsonable_encoder(MealMethods(DB).get_meal(id)), status_code=status.HTTP_200_OK)


@meals_router.post("/", status_code=201)
def add_meal(new_meal: Food):
    """ Añade un nuevo alimento a la base de datos. """
    MealMethods(DB).add_new_meal(new_meal_data=new_meal)

    return JSONResponse(content={"message": "Se ha añadido una nueva comida!"}, status_code=201)


@meals_router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_meal(id: int, data: Food):
    """ Puedes actualizar los atributos de una comida solamente especificando el id único de la comida. """
    MealMethods(DB).update_meal_attribute(id=id, data_to_update=data)

    return JSONResponse(content={"message": "Comida actualizada satisfactoriamente."}, status_code=status.HTTP_200_OK)


@meals_router.delete("/", status_code=status.HTTP_200_OK)
def delete_all(token: Annotated[str, Depends(oauth2_bearer)]):
    """ USAR BAJO RESPONSABILIDAD. Puedes eliminar todos los alimentos almacenados de la base de datos. """
    MealMethods(DB).delete_all_meals_stored()

    return JSONResponse(content={"message": "Todas las comidas almacenadas fueron eliminadas satisfactoriamente."}, status_code=status.HTTP_200_OK)

