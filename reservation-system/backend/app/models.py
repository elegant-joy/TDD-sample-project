from pydantic import BaseModel, Field
from datetime import datetime


class ReservationBase(BaseModel):
    """予約の基本となる共通フィールド"""

    resource_id: str = Field(..., description="予約するリソースのID (例: 'CONF-A')")
    start_time: datetime = Field(..., description="予約開始日時")
    end_time: datetime = Field(..., description="予約終了日時")
    user_name: str = Field(..., description="予約者名")


class ReservationCreate(ReservationBase):
    """予約作成時にクライアントから受け取るモデル"""

    # ReservationBaseのフィールドをそのまま使用
    pass


class Reservation(ReservationBase):
    """データベースから取得し、クライアントへ返すモデル (ID付き)"""

    id: int = Field(..., description="システムが採番した一意の予約ID")

    # Pydantic v2では、ORMモードは不要になりました。
    # class Config:
    #     orm_mode = True
