from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette import status
from models.food import Meal as MealModel
from schemas.meal_pydantic_model import Food
from exceptions.meal_exceptions import MEAL_ID_EXCEPTION


class MealMethods:
    def __init__(self, db) -> None:
        self.db = db

    
    def get_all_meals_available(self):
        all_meals = self.db.query(MealModel).all()

        if not all_meals:
            return JSONResponse(content={"message": "No se encontró información en la base de datos."}, status_code=status.HTTP_404_NOT_FOUND)

        return all_meals


    def get_meal(self, id: int):
        meal = self.db.query(MealModel).filter(id == MealModel.meal_id).first()

        if not meal:
            raise MEAL_ID_EXCEPTION

        return meal


    def add_new_meal(self, new_meal_data: Food):
        new_meal = MealModel(**jsonable_encoder(dict(new_meal_data)))

        self.db.add(new_meal)
        self.db.commit()


    def delete_all_meals_stored(self):
        self.db.query(MealModel).delete()
        self.db.commit()
