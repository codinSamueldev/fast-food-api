from config.database import Base
from sqlalchemy import Column, Integer, Float, String

class Meal(Base):

    __tablename__ = "Meals"

    meal_id = Column(Integer, primary_key=True)
    meal_name = Column(String)
    meal_ingredients = Column(String)
    meal_price = Column(Float(10, 3))
