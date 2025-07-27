import unittest
from datetime import datetime, timedelta
# FastAPIのテストにはTestClientを使うのが便利ですが、
# まずは純粋なロジックのテストから始めます。


# 例：予約衝突ロジックのテストクラス
"""

1. 最も重要な失敗ケース：「予約が衝突する」テスト
- 既存の予約と時間が完全に重複する新しい予約は作成できない、というテスト。これが最初の「Red (失敗)」になるべきテストです。

2. 成功ケース：「予約が衝突しない」テスト
- 既存の予約と時間が全く重ならない新しい予約は作成できる、というテスト。これにより、何でもかんでもブロックするような誤った実装を防ぎます。

3. エッジケース：「境界値」のテスト
- 既存の予約の終了時刻と、新しい予約の開始時刻が全く同じ場合（衝突しないはず）。
- 既存の予約の開始時刻と、新しい予約の終了時刻が全く同じ場合（衝突しないはず）。

4. 不正な入力データに対するテスト

- 予約の終了時刻が開始時刻よりも前になっている、といった無効なデータは弾かれるべき、というテスト。
"""


# --- この部分は、後で app/routers/reservations.py などに実装するロジックの仮置き ---
# TDDのサイクル：まずテストを書き、それをパスさせるためにこの関数を実装します。
def create_reservation_logic(new_reservation, existing_reservations):
    """
    Args:
        new_reservation (dict): {'start_time': datetime, 'end_time': datetime}
        existing_reservations (list[dict]): 既存の予約リスト

    Returns:
        dict: 作成された予約情報

    Raises:
        ValueError: 予約が衝突した場合や、データが不正な場合
    """
    # 最初はわざと実装しないか、常に成功させる
    # self.fail()をパスさせるために、まずは例外を発生させる実装から始める
    raise NotImplementedError("This function is not yet implemented.")


# --------------------------------------------------------------------------------


class TestReservationLogic(unittest.TestCase):
    def setUp(self):
        """各テストの前に実行される共通のセットアップ"""
        # 基準となる既存の予約 (10:00 - 11:00)
        self.base_time = datetime(2025, 8, 1, 10, 0, 0)
        self.existing_reservations = [
            {
                "resource_id": "CONF-A",
                "start_time": self.base_time,
                "end_time": self.base_time + timedelta(hours=1),
            }
        ]

    def test_create_reservation_fails_if_overlap_exists(self):
        """
        [RED] Test Case 1: 既存の予約と完全に重複する場合、ValueErrorを発生させる
        (10:30-11:30 の予約は 10:00-11:00 と衝突する)
        """
        new_reservation = {
            "resource_id": "CONF-A",
            "start_time": self.base_time + timedelta(minutes=30),
            "end_time": self.base_time + timedelta(hours=1, minutes=30),
        }

        # create_reservation_logic を呼び出すと ValueError が発生することを期待する
        with self.assertRaises(ValueError):
            create_reservation_logic(new_reservation, self.existing_reservations)

    def test_create_reservation_succeeds_if_no_overlap(self):
        """
        [GREEN] Test Case 2: 既存の予約と重複しない場合、予約が作成される (例外が発生しない)
        (11:00-12:00 の予約は 10:00-11:00 と衝突しない)
        """
        new_reservation = {
            "resource_id": "CONF-A",
            "start_time": self.base_time + timedelta(hours=1),
            "end_time": self.base_time + timedelta(hours=2),
        }

        try:
            # この呼び出しで例外が発生しないことを確認
            created = create_reservation_logic(
                new_reservation, self.existing_reservations
            )
            # 成功した場合は、渡したデータが何らかの形で返されることを期待しても良い
            self.assertEqual(created["start_time"], new_reservation["start_time"])
        except ValueError:
            self.fail("予約が衝突しないはずなのにValueErrorが発生しました")

    def test_create_reservation_fails_if_end_time_is_before_start_time(self):
        """
        [RED] Test Case 3: 終了時刻が開始時刻より前の予約はValueErrorを発生させる
        """
        invalid_reservation = {
            "resource_id": "CONF-A",
            "start_time": self.base_time,
            "end_time": self.base_time - timedelta(minutes=10),  # 終了時刻が前
        }
        with self.assertRaises(ValueError):
            create_reservation_logic(invalid_reservation, self.existing_reservations)


if __name__ == "__main__":
    unittest.main()
