from pydantic import BaseModel, Field

class Food(BaseModel):

    meal_id: int | None = None
    meal_name: str = Field(max_length=50)
    meal_ingredients: str = Field(min_length=5, max_length=90)
    meal_price: float

    class Config:
        json_schema_extra = {
            "example": {
                "meal_name": "Sandwich",
                "meal_ingredients": "Pan/Jamón/Lechuga/Tomate",
                "meal_price": 5.99
            }
        }

