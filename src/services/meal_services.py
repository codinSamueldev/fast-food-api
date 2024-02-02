from models.food import Meal
from exceptions.meal_exceptions import MEAL_ID_EXCEPTION


class MealMethods:
    def __init__(self, db) -> None:
        self.db = db

    
    def get_all_meals_available(self):
        all_meals = self.db.query(Meal).all()

        return all_meals


    def get_meal(self, id: int):
        meal = self.db.query(Meal).filter(id == Meal.meal_id).first()

        if not meal:
            raise MEAL_ID_EXCEPTION

        return meal

