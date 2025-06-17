import unittest
import tempfile
import os
from repository import FileRouteRepository
from exceptions import DataParsingError

CSV_HEADER = "id,name,region,start_lat,start_lon,end_lat,end_lon,length_km,elevation_gain,difficulty,terrain_type,tags\n"

class TestFileRouteRepository(unittest.TestCase):

    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', newline='')
        self.test_file.write(CSV_HEADER)
        self.test_file.write(
            "1,Test Route,Region,49.0,20.0,49.1,20.1,8.0,400,2,forest,tag1\n"
        )
        self.test_file.write(
            "2,Another Route,Region,49.2,20.2,49.3,20.3,10.0,600,3,mountain,tag2\n"
        )
        self.test_file.close()

    def tearDown(self):
        os.unlink(self.test_file.name)

    def test_get_all_valid(self):
        repo = FileRouteRepository(self.test_file.name)
        routes = repo.get_all()
        self.assertEqual(len(routes), 2)
        self.assertEqual(routes[0].name, "Test Route")

    def test_invalid_data(self):
        with open(self.test_file.name, 'w', encoding='utf-8') as f:
            f.write(CSV_HEADER)
            f.write("1,Invalid,Region,49.0,20.0,49.1,20.1,8.0,400,not_a_number,forest,tag1\n")

        repo = FileRouteRepository(self.test_file.name)
        with self.assertRaises(DataParsingError):
            repo.get_all()

    def test_empty_file(self):
        with open(self.test_file.name, 'w', encoding='utf-8') as f:
            f.write(CSV_HEADER)

        repo = FileRouteRepository(self.test_file.name)
        self.assertEqual(repo.get_all(), [])

    def test_file_not_found(self):
        repo = FileRouteRepository("non_existent.csv")
        with self.assertRaises(FileNotFoundError):
            repo.get_all()