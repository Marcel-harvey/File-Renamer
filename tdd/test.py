import unittest
from Backend.Json_handler import *


class JsonSetDirectoriesTest(unittest.TestCase):
    def test_if_empty_location_string(self):
        set_directory = SetDirectoryManager('', 'E:\\Anime')
        self.assertEqual(set_directory.confirm_directory(), 'No Location entered')

    def test_if_empty_destination_string(self):
        set_directory = SetDirectoryManager('C:\\Users\\Marcel\\Downloads', '')
        self.assertEqual((set_directory.confirm_directory()), 'No Destination entered')

    def test_if_invalid_location_was_given(self):
        set_directory = SetDirectoryManager('c use marcel downloads', 'e animation')
        self.assertEqual(set_directory.confirm_directory(), 'Invalid Directory given')

    def test_if_invalid_destination_was_given(self):
        set_directory = SetDirectoryManager('c use marcel downloads', 'e animation')
        self.assertEqual(set_directory.confirm_directory(), 'Invalid Directory given')

    def test_if_valid_directories_was_given(self):
        set_directory = SetDirectoryManager('C:\\Users\\Marcel\\Downloads', 'E:\\Anime')
        self.assertEqual(set_directory.confirm_directory(), False)

    def test_if_json_has_stored_in_file(self):
        has_stored = SetDirectoryManager('C:\\Users\\Marcel\\Downloads', 'E:\\Anime').set_json_directories()
        is_valid_location = GetDirectoryManager().get_location()
        is_valid_destination = GetDirectoryManager().get_destination()

        self.assertTrue(has_stored, True)
        self.assertIsNot(is_valid_location, not None)
        self.assertIsNot(is_valid_destination, not None)


class JsonGetDirectoriesTest(unittest.TestCase):
    def setUp(self):
        self.get_directories = GetDirectoryManager()
        self.location = self.get_directories.get_location()
        self.destination = self.get_directories.get_destination()

    def test_if_has_location(self):
        self.assertIsInstance(self.location, str)

    def test_if_has_destination(self):
        self.assertIsInstance(self.destination, str)


class JsonUpdateDirectoriesTest(unittest.TestCase):
    def setUp(self):
        self.update_directories = UpdateDirectoryManager('C:\\Users\\Marcel\\Documents', 'E:\\OTHER')
        self.new_directories = self.update_directories.update_directories()

        # Gets the directories in the Json file AFTER it has being updated
        self.get_directories = GetDirectoryManager()
        self.location_in_file = self.get_directories.get_location()
        self.destination_in_file = self.get_directories.get_destination()

    def test_if_location_updated(self):
        self.assertEqual(self.new_directories[0], self.location_in_file)

    def test_if_destination_updated(self):
        self.assertEqual(self.new_directories[1], self.destination_in_file)


if __name__ == '__main__':
    unittest.main()
