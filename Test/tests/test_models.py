import unittest
from models import Route

class TestModels(unittest.TestCase):
    def test_valid_route(self):
        route = Route(
            id=1,
            name="Test",
            region="Tatry",
            start_lat="49.0",
            start_lon="20.0",
            end_lat="49.1",
            end_lon="20.1",
            length_km="10.5",
            elevation_gain="500",
            difficulty="3",
            terrain_type="mountain",
            tags="view,scenic"
        )
        self.assertEqual(route.name, "Test")
        self.assertEqual(route.difficulty, 3)
        self.assertIn("view", route.tags)

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            Route(
                id=2,
                name="Invalid",
                region="Tatry",
                start_lat="49.0",
                start_lon="20.0",
                end_lat="49.1",
                end_lon="20.1",
                length_km="-5",
                elevation_gain="300",
                difficulty="2",
                terrain_type="forest",
                tags=""
            )

    def test_invalid_difficulty(self):
        with self.assertRaises(ValueError):
            Route(
                id=3,
                name="Invalid Diff",
                region="Tatry",
                start_lat="49.0",
                start_lon="20.0",
                end_lat="49.1",
                end_lon="20.1",
                length_km="5.0",
                elevation_gain="300",
                difficulty="10",
                terrain_type="forest",
                tags=""
            )

    def test_user_preference(self):
        from models import UserPreference
        pref = UserPreference(max_difficulty=2, terrain="forest")
        self.assertEqual(pref.max_difficulty, 2)
        self.assertEqual(pref.terrain, "forest")