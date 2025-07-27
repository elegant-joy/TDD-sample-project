import unittest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

# FastAPIアプリケーションのインスタンスをインポート
from app.main import app


class TestReservationAPI(unittest.TestCase):
    def setUp(self):
        """各テストの前に実行され、TestClientをセットアップし、DBをクリアする"""
        self.client = TestClient(app)
        # 各テストが独立するように、開始前に全予約を削除
        self.client.delete("/reservations/all")

        # 基準となる予約を1件作成しておく
        self.base_time = datetime(2025, 8, 1, 10, 0, 0)
        # このPOSTリクエストが成功することがテスト全体の前提
        response = self.client.post(
            "/reservations/",
            json={
                "resource_id": "CONF-A",
                "start_time": self.base_time.isoformat(),
                "end_time": (self.base_time + timedelta(hours=1)).isoformat(),
                "user_name": "Initial User",
            },
        )
        # ここでアサーションを追加して、そもそもsetUpが成功しているか確認するのも有効
        self.assertEqual(
            response.status_code, 201, "Failed to setup initial reservation."
        )

    def test_create_reservation_fails_on_conflict(self):
        """API Test 1: 既存の予約と衝突する場合、409 Conflictを返す"""
        overlapping_payload = {
            "resource_id": "CONF-A",  # 同じリソース
            "start_time": (self.base_time + timedelta(minutes=30)).isoformat(),
            "end_time": (self.base_time + timedelta(hours=1, minutes=30)).isoformat(),
            "user_name": "Conflict User",
        }

        response = self.client.post("/reservations/", json=overlapping_payload)

        # ステータスコードが409であることを確認
        self.assertEqual(response.status_code, 409)
        # エラーメッセージに "conflict" が含まれることを確認
        self.assertIn("conflict", response.json()["detail"])

    def test_create_reservation_succeeds_if_no_conflict(self):
        """API Test 2: 既存の予約と衝突しない場合、201 Createdを返す"""
        non_overlapping_payload = {
            "resource_id": "CONF-A",  # 同じリソースでも時間が違う
            "start_time": (self.base_time + timedelta(hours=1)).isoformat(),
            "end_time": (self.base_time + timedelta(hours=2)).isoformat(),
            "user_name": "Next User",
        }

        response = self.client.post("/reservations/", json=non_overlapping_payload)

        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data["user_name"], "Next User")
        self.assertIn("id", response_data)

    def test_create_reservation_succeeds_for_different_resource(self):
        """API Test 3: 時間が重複していても、リソースが異なれば成功する"""
        payload_for_other_resource = {
            "resource_id": "CONF-B",  # 異なるリソース
            "start_time": (self.base_time + timedelta(minutes=30)).isoformat(),
            "end_time": (self.base_time + timedelta(hours=1, minutes=30)).isoformat(),
            "user_name": "Other Resource User",
        }

        response = self.client.post("/reservations/", json=payload_for_other_resource)
        self.assertEqual(response.status_code, 201)

    def test_create_reservation_fails_if_end_time_is_before_start_time(self):
        """API Test 4: 終了時刻が開始時刻より前の場合、409 Conflictを返す"""
        invalid_time_payload = {
            "resource_id": "CONF-A",
            "start_time": self.base_time.isoformat(),
            "end_time": (self.base_time - timedelta(minutes=10)).isoformat(),
            "user_name": "Invalid Time User",
        }

        response = self.client.post("/reservations/", json=invalid_time_payload)
        self.assertEqual(response.status_code, 409)
        self.assertIn("End time must be after start time", response.json()["detail"])
