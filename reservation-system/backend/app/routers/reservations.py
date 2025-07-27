from fastapi import APIRouter, HTTPException, status
from datetime import datetime

# from models import models.Reservation
from .. import models

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
)


# --- 偽物のインメモリデータベース ---
# アプリケーションが起動している間だけデータを保持します。
# テストのたびにリセットする必要があります。
db_reservations: list[models.Reservation] = []


def check_reservation_conflict(
    new_reservation: models.Reservation,
    existing_reservations: list[models.Reservation],
) -> None:
    if new_reservation.end_time <= new_reservation.start_time:
        raise ValueError("End time must be after start time.")

    for existing in existing_reservations:
        if (
            new_reservation.start_time < existing.end_time
            and new_reservation.end_time > existing.start_time
        ):
            # 別のリソースの予約とは衝突しない
            if new_reservation.resource_id == existing.resource_id:
                raise ValueError(
                    f"models.Reservation conflict detected for resource {new_reservation.resource_id}."
                )


@router.post(
    "/", response_model=models.Reservation, status_code=status.HTTP_201_CREATED
)
def create_reservation(reservation_date: models.ReservationCreate):
    """新しい予約を作成するエンドポイント"""
    try:
        check_reservation_conflict(reservation_date, db_reservations)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    # 衝突がなければ、"データベース"に保存
    # 実際のアプリではここでDBの採番IDなどをセットする
    new_id = len(db_reservations) + 1
    created_reservation = models.Reservation(
        id=new_id,
        **reservation_date.model_dump(),  # Pydantic v2
    )
    db_reservations.append(created_reservation)

    return created_reservation


# テストを容易にするための、DBをリセットするエンドポイント（開発用）
@router.delete("/all", status_code=status.HTTP_204_NO_CONTENT)
def clear_all_reservations():
    """全ての予約を削除する（テスト用）"""
    db_reservations.clear()
    return None
