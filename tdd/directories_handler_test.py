import unittest
from Backend.Directory_handler import *
# Test name for the mock tests
# [Golumpa]The Detective Is Already Dead - 05 (Tantei wa Mou, Shindeiru.) [FuniDub 1080p x264 AAC] [6B4D2FBC].1080.mp4
# [Golumpa]Test case - 05 (Tantei wa Mou, Shindeiru.) [FuniDub 1080p x264 AAC] [6B4D2FBC].1080.mp4


class DirectoryFindName(unittest.TestCase):
    def test_if_name_variation_one_is_correct(self):
        name = Finder('[test]name - 01 (test) [test 1000] [1test23test').get_name()

        self.assertEqual(name, 'name')

    def test_if_name_variation_two_is_correct(self):
        name = Finder('(test)name - 01 (test) [test 1000] [1test23test').get_name()

        self.assertEqual(name, 'name')

    def test_if_name_variation_three_is_correct(self):
        name = Finder('name- 01 (test) [test 1000] [1test23test').get_name()

        self.assertEqual(name, 'name')

    def test_if_name_variation_four_is_correct(self):
        name = Finder('[test]   name - 01 (test) [test 1000] [1test23test').get_name()

        self.assertEqual(name, 'name')

    def test_if_name_variation_five_is_correct(self):
        name = Finder('[Golumpa] Tokyo Revengers - 10 [CR-Dub 1080p x264 AAC] [56B97559].1080.mp4').get_name()

        self.assertEqual(name, 'Tokyo Revengers')

    def test_if_name_variation_six_is_correct(self):
        name = Finder('[CR] Tokyo Revengers (English Dub) - 18 [1080p].1080.mp4').get_name()

        self.assertEqual(name, 'Tokyo Revengers')

    def test_if_episode_variation_one_is_correct(self):
        episode = Finder('[test]name - 01 (test) [test 1000] [1test23test').get_episode_number()

        self.assertEqual(episode, '01')

    def test_if_episode_variation_two_is_correct(self):
        episode = Finder('[test]name - S08E01 (test) [test 1000] [1test23test').get_episode_number()

        self.assertEqual(episode, '01')

    def test_if_episode_variation_three_is_correct(self):
        episode = Finder('[test]name -01 (test) [test 1000] [1test23test').get_episode_number()

        self.assertEqual(episode, '01')

    def test_if_episode_variation_four_is_correct(self):
        episode = Finder('[test]name -S08E01 (test) [test 1000] [1test23test').get_episode_number()

        self.assertEqual(episode, '01')

    def test_if_episode_variation_five_is_correct(self):
        episode = Finder('[Golumpa] Tokyo Revengers - 10 [CR-Dub 1080p x264 AAC] [56B97559].1080').get_episode_number()

        self.assertEqual(episode, '10')


class DirectoryHandlerTests(unittest.TestCase):
    # Check if you get the full file name of the video
    def test_if_file_location_is_correct(self):
        file = GetDirectoryPath('C:\\Users\\Marcel\\Downloads').get_path()

        self.assertEqual(
            file, '[Golumpa]Test case - 05 (Tantei wa Mou, Shindeiru.) [FuniDub 1080p x264 AAC] [6B4D2FBC].1080'
        )

    def test_if_old_name_path_is_correct_for_source(self):
        # This test does require a mp4 file in the download's directory to work as it is not a mock test
        rename_data = Handler(
            'C:\\Users\\Marcel\\Downloads', 'E:\\Anime', 'Dubbed', '1',
            '[Golumpa]Test case - 05 (Tantei wa Mou, Shindeiru.) [FuniDub 1080p x264 AAC] [6B4D2FBC].1080.mp4'
        ).rename()

        old_name = rename_data[0]
        new_name = rename_data[1]

        self.assertEqual(new_name, 'C:\\Users\\Marcel\\Downloads\\Test case Season 1 English Dubbed Episode - 05.mp4')
        self.assertEqual(
            old_name, 'C:\\Users\\Marcel\\Downloads\\'
                      '[Golumpa]Test case - 05 (Tantei wa Mou, Shindeiru.) [FuniDub 1080p x264 AAC] [6B4D2FBC].1080.mp4'
        )
        # Renames the file back to its original name, this is used for testing purposes only
        # If test has passed, it means it works
        os.rename(new_name, old_name)

    def test_if_directory_is_created(self):
        is_dir_created = Handler(
            'C:\\Users\\Marcel\\Downloads', 'E:\\Anime', 'Dubbed', '1',
            '[Golumpa]Test case - 05 (Tantei wa Mou, Shindeiru.) [FuniDub 1080p x264 AAC] [6B4D2FBC].1080.mp4'
        ).create_directory()

        self.assertTrue(is_dir_created, True)

    def test_if_file_moves_to_directory(self):
        # This test may take some time, as it actually moves the file from downloads to its desired location
        # This test requires a video file in the downloads directory
        has_file_moved = Handler(
            'C:\\Users\\Marcel\\Downloads', 'E:\\Anime', 'Dubbed', '1',
            '[Golumpa]Test case - 05 (Tantei wa Mou, Shindeiru.) [FuniDub 1080p x264 AAC] [6B4D2FBC].1080.mp4'
        ).move()

        self.assertTrue(has_file_moved, True)

    def test_if_file_has_renamed_if_user_not_satisfied_with_name(self):
        user_given_name = 'User\'s name'
        mini_handler = Handler(
            'C:\\Users\\Marcel\\Downloads', 'E:\\Anime', 'Dubbed', '1',
            '[Golumpa]Test case - 05 (Tantei wa Mou, Shindeiru.) [FuniDub 1080p x264 AAC] [6B4D2FBC].1080.mp4'
        )

        other_name = mini_handler.get_name()
        name_received_from_function = mini_handler.get_name(user_given_name)

        self.assertNotEqual(name_received_from_function, other_name)
