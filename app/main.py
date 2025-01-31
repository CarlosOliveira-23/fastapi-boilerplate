from fastapi import FastAPI
from app.api.endpoints import auth, users

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
def root():
    return {"message": "Boilerplate FastAPI funcionando!"}
