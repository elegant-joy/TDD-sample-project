from fastapi import FastAPI
from .routers import reservations

app = FastAPI()

app.include_router(reservations.router)


@app.get("/")
def read_root():
    return {"message": "Resource Reservation API"}
