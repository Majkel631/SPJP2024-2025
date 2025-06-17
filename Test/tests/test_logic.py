import unittest
import tempfile
import os
from repository import FileRouteRepository
from logic import RouteRecommender
from models import UserPreference

CSV_HEADER = "id,name,region,start_lat,start_lon,end_lat,end_lon,length_km,elevation_gain,difficulty,terrain_type,tags\n"

class TestRouteRecommender(unittest.TestCase):

    def setUp(self):
        self.file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', newline='')
        self.file.write(CSV_HEADER)
        self.file.write("1,Easy Forest,Region,49.0,20.0,49.1,20.1,5.0,100,1,forest,tag\n")
        self.file.write("2,Hard Mountain,Region,49.0,20.0,49.1,20.1,10.0,800,5,mountain,tag\n")
        self.file.write("3,Mid Mountain,Region,49.0,20.0,49.1,20.1,8.0,500,3,mountain,tag\n")
        self.file.close()

        self.repo = FileRouteRepository(self.file.name)
        self.recommender = RouteRecommender(self.repo)

    def tearDown(self):
        os.unlink(self.file.name)

    def test_filtering(self):
        pref = UserPreference(max_difficulty=3, terrain="mountain")
        results = self.recommender.recommend(pref)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Mid Mountain")

    def test_no_matches(self):
        pref = UserPreference(max_difficulty=1, terrain="rocky_mountains")
        results = self.recommender.recommend(pref)
        self.assertEqual(results, [])