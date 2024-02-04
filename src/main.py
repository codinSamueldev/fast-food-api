from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette import status

from routers import meals
from routers.security import jwt_security_flow
from config.database import engine, Base
from middleware.error_handler import ErrorHandler


app = FastAPI()
app.include_router(meals.meals_router)
app.include_router(jwt_security_flow.security_router)
# app.add_middleware(ErrorHandler)
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.title="Fast-food API"
app.version="1.0"

Base.metadata.create_all(bind=engine)


@app.get("/", status_code=status.HTTP_200_OK, tags=["Home-page"])
def home_page():
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="es">
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Kanit&display=swap');
        </style>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fast-food</title>
        <link rel="icon" href="static/python_icon.png">
        <a style="visibility: hidden;" target="_blank" href="https://icons8.com/icon/YX03OUiHE3rz/python">Python</a> icon by <a style="visibility: hidden;" target="_blank" href="https://icons8.com">Icons8</a>
    </head>
    <body style="font-family: 'Kanit', sans-serif; margin: 0; padding: 0; background: black;">
        <main style="text-align: center; color: white;">
            <h1>PAMICASA</h1>
            <article style="display: flex; flex-direction: row; flex-wrap: wrap; justify-content: center; align-items: center; gap: 1rem;">
                <section>
                    <div style="background: grey; padding: 0.5rem; border: 3px solid greenyellow; border-radius: 3px; box-shadow: 9px 9px yellow;">
                        <h2>Nuestros delicias &#127791;</h2>
                        <ul style="list-style: none; margin: 0; padding: 0;">
                            <li>Pequeña Mac</li>
                            <li>Perros</li>
                            <li>Tacos</li>
                        </ul>
                    </div>
                </section>
                <section>
                    <div style="background: grey; padding: 0.5rem; border: 3px solid greenyellow; border-radius: 3px; box-shadow: 9px 9px yellow;">
                        <h2>Desde 2024 &#128080;</h2>
                        <ul style="list-style: none; margin: 0; padding: 0;">
                            <li>Con un gran espacio para descansar</li>
                            <li>Agregando nuestra receta <b>secreta</b>&#129323;</li>
                            <li>Juegos de arcade</li>
                        </ul>
                    </div>
                </section>
            </article>
            <figure style="width: 50%; display: block; margin-left: auto; margin-right: auto; padding: 0.5rem 0 6rem 0; ">
                <img src="static/small_mac.jpg" alt="pequeña mac" style="width: -webkit-fill-available; border-radius: 1.51rem">
                <figcaption>La pequeña mac &#129401;</figcaption>
            </figure>
        </main>
        <footer style="color: #fff; display: flex; justify-content: center; height: auto; padding: 1.6rem; background: #fa9500; position: fixed; bottom: 0; left: 0; right: 0; height: 2rem;">
            <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noopener noreferrer" style="color: white; font-size: 2rem;">Docs &#128424;&#65039;</a>
        </footer>
    </body>
</html>
""", status_code=status.HTTP_200_OK)


