from fastapi import HTTPException

MEAL_ID_EXCEPTION = HTTPException(status_code=404, detail="Meal ID not found :c")
