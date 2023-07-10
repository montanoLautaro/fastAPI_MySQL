from fastapi import FastAPI
from routers import users, entertainments

app = FastAPI()

app.include_router(users.router)
app.include_router(entertainments.router)


@app.get("/")
async def saludo():
    return "Online."
