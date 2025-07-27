import unittest
# FastAPIのテストにはTestClientを使うのが便利ですが、
# まずは純粋なロジックのテストから始めます。


# 例：予約衝突ロジックのテストクラス
class TestReservationLogic(unittest.TestCase):
    def test_detect_reservation_conflict(self):
        # 1. 最初に失敗するテストを書く (Red)
        # 例: 既存の予約 (10:00-11:00) がある
        #     新しい予約 (10:30-11:30) を追加しようとすると衝突を検知できるか
        self.fail("まだ実装されていません")


if __name__ == "__main__":
    unittest.main()
