def create_reservation_logic(
    new_reservation: dict, existing_reservations: list[dict]
) -> dict:
    """
    新しい予約が有効か（データ形式、時間的衝突）を検証し、
    問題がなければ予約情報を返す。

    Raises:
        ValueError: 予約が衝突した場合や、データが不正な場合
    """
    # Test Case 3: 終了時刻が開始時刻より前の予約は不正
    if new_reservation["end_time"] <= new_reservation["start_time"]:
        raise ValueError("End time must be after start time.")

    # Test Case 1 & 2: 既存の予約と時間的な衝突がないかチェック
    for existing in existing_reservations:
        # 衝突条件:
        # 新規予約の開始時刻 < 既存予約の終了時刻 AND 新規予約の終了時刻 > 既存予約の開始時刻
        # ex) 11:00 < 11:30 and 12:00 > 10:30
        # これが成立する場合、時間帯が重なっていると判断できる
        if (
            new_reservation["start_time"] < existing["end_time"]
            and new_reservation["end_time"] > existing["start_time"]
        ):
            raise ValueError("Reservation conflict detected.")

    # 全てのチェックをパスした場合、新しい予約情報をそのまま返す
    return new_reservation
