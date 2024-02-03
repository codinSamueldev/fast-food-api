from fastapi import HTTPException

MEAL_ID_EXCEPTION = HTTPException(status_code=404, detail="Meal ID not found :c")
NOT_FOUND_EXCEPTION = HTTPException(status_code=404, detail="No se encontró información en la base de datos.")
