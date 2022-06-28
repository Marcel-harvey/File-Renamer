import os
import glob
import re
import shutil
from pathlib import Path


class GetDirectoryPath:
    def __init__(self, location):
        self.location = location

    def get_path(self):
        path = f'{self.location}**\\*.mp4'
        anime_list = []

        for file in glob.iglob(path, recursive=True):
            anime_list.append(os.path.basename(file))

        return anime_list


class Finder:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_name(self, *args):
        pattern = re.compile(r'^\s?([\[|(?][a-zA-Z]*[]|)?])?[.\s]?([a-zA-Z\s]+)\s?([\[|(]?[a-zA-Z\s]*[]|)]?)\s?-')
        matches = pattern.finditer(self.file_name)

        if not args:
            for match in matches:
                return str(match.group(2).strip())

        else:
            return str(args[0].strip())

    def get_episode_number(self):
        pattern = re.compile(r'(-\s?)([a-zA-Z]*\d*[a-zA-Z])?(\d*)')
        matches = pattern.finditer(self.file_name)

        for match in matches:
            return match.group(3).strip()


class Handler(Finder):

    def __init__(self, location, destination, language, season, file_name, *args):
        super().__init__(file_name)
        if not args:
            self._renamed_name = super().get_name()

        elif args:
            self._renamed_name = super().get_name(args[0])

        self.episode = super().get_episode_number()
        self.location = location
        self.destination = destination
        self.season = season
        self.language = language
        self.file_name = file_name
        self.anime_fullname = \
            f'{self._renamed_name} Season {self.season} English {self.language} Episode - {self.episode}.mp4'

    def create_directory(self):
        directory_path = Path(f'{self.destination}\\{self._renamed_name}')
        directory_path.mkdir(exist_ok=True)

        season_directory_path = Path(f'{self.destination}\\{self._renamed_name}\\Season {self.season}')
        season_directory_path.mkdir(exist_ok=True)

        if season_directory_path.is_dir():
            return True
        else:
            return False

    def rename(self):
        source = f'{self.location}\\{self.file_name}'
        new_name = f'{self.location}\\{self.anime_fullname}'

        try:
            os.rename(source, new_name)
            return [source, new_name]
        except OSError as e:
            print(e)
            return [None, None]

    def move(self):
        location = f'{self.location}\\{self.anime_fullname}'
        destination = f'{self.destination}\\{self._renamed_name}\\Season {self.season}'

        check_if_dir_exists = Path(f'{self.destination}\\{self._renamed_name}\\Season {self.season}')

        if check_if_dir_exists.is_dir():
            try:
                shutil.move(location, destination)
                return True
            except shutil.Error:
                print(shutil.Error)
                return False

# https://stackoverflow.com/questions/7336096/python-glob-without-the-whole-path-only-the-filename
# https://www.geeksforgeeks.org/python-list-files-in-a-directory/
