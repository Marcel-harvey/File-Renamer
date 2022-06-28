import json
import os
from dataclasses import dataclass


@dataclass
class SetDirectoryManager:

    def __init__(self, location, destination):
        self.location = location
        self.destination = destination

    def confirm_directory(self):

        if self.location == '':
            return 'No Location entered'

        if self.destination == '':
            return 'No Destination entered'

        if not os.path.isdir(self.location) and not os.path.isdir(self.destination):
            return 'Invalid Directory given'

        elif os.path.isdir(self.location) and os.path.isdir(self.destination):
            return False

    def set_json_directories(self):
        try:
            with open(r'./Json/dir.json', 'r+') as file:
                data = json.load(file)
                anime = {
                    'location': self.location,
                    'destination': self.destination
                }

                data['anime'].append(anime)
                file.seek(0)

                json.dump(data, file, ensure_ascii=True, sort_keys=True, indent=4)
                return True
        except OSError as e:
            print(e)
            return False


@dataclass
class GetDirectoryManager:

    def __init__(self):
        with open(r'./Json/dir.json', 'r') as directories:
            self.data = json.load(directories)

    def get_location(self):
        try:
            return self.data['anime'][0]['location']
        except IndexError:
            return None

    def get_destination(self):
        try:
            return self.data['anime'][0]['destination']
        except IndexError:
            return None


class UpdateDirectoryManager:

    def __init__(self, location, destination):
        self.location = location
        self.destination = destination

    def update_directories(self):
        with open(r'./Json/dir.json', 'r+') as directories:
            data = json.load(directories)
            try:
                data['anime'][0]['location'] = self.location
                data['anime'][0]['destination'] = self.destination

                directories.seek(0)
                json.dump(data, directories, sort_keys=True, ensure_ascii=False, indent=4)
                directories.truncate()

                return [self.location, self.destination]

            except IndexError:
                return None
