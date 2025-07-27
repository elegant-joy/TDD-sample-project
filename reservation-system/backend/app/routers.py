from fastapi import APIRouter
from .. import models

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
)


# TDDでこれから実装するエンドポイント
@router.post("/", response_model=models.Reservation)
def create_reservation(reservation: models.ReservationCreate):
    # ここにロジックを実装していく
    pass


@router.get("/")
def get_reservations_for_resource(resource_id: str):
    # ここにロジックを実装していく
    pass
