from Backend.Json_handler import *
from Backend.Directory_handler import *


def main():
    while True:
        users_choice = input('\nDo you want to wait, view\\change path or quit? (w\\c\\q)\n')

        if users_choice == 'w':
            start_process = input('\nPress enter when new files arrive or input "s" to stop\n')

            if start_process == 's':
                continue

            elif start_process == '':
                def mini_directory_manager():
                    directory_location = GetDirectoryManager().get_location()
                    directory_destination = GetDirectoryManager().get_destination()

                    # If there is no directories in the Json file, this will add a new one
                    if directory_destination is None or directory_location is None:
                        new_location = input('\nPlease enter the path where the downloads can be found\n')
                        new_destination = input(
                            '\nPlease enter the path of the folder where you want to store the anime\n'
                        )

                        set_manager = SetDirectoryManager(new_location, new_destination)
                        is_directory_set = set_manager.confirm_directory()

                        if is_directory_set:    # If string is valid, returns False
                            print(is_directory_set)
                            mini_directory_manager()

                        has_created_directory = set_manager.set_json_directories()
                        if has_created_directory:
                            print('\nDirectories has being successfully saved')

                    else:
                        return

                mini_directory_manager()

            # Starting the process of renaming and moving the file
            def season_of_anime():
                try:
                    what_is_the_season = int(input('What season is this of the anime\n'))
                except ValueError:
                    print('\nPlease enter a number only')
                    season_of_anime()
                else:
                    return what_is_the_season

            season = season_of_anime()

            def language_of_anime():
                what_is_the_language = input('Is the anime Dubbed or Subbed? (d\\s)\n')

                if what_is_the_language == 'd':
                    return 'Dubbed'

                elif what_is_the_language == 's':
                    return 'Subbed'

                else:
                    print('\nPlease enter a valid choice')
                    language_of_anime()

            language = language_of_anime()

            location = GetDirectoryManager().get_location()
            destination = GetDirectoryManager().get_destination()
            original_name_of_anime_list = GetDirectoryPath(location).get_path()
            original_name_of_anime = original_name_of_anime_list[0]
            new_anime_name = Finder(original_name_of_anime).get_name()

            def confirm_name_of_anime(*args):
                nonlocal new_anime_name
                if not args:
                    confirm_name = input(f'File will be renamed to: {new_anime_name}\n'
                                         f'Is this correct? (y\\n)\n')
                    if confirm_name == 'n':
                        new_name_input = input('What would you like to call the anime then?\n')
                        confirm_name_of_anime(new_name_input)

                elif args:
                    new_anime_name = args[0]
                    confirm_name1 = input(f'File will be renamed to: {new_anime_name}\n'
                                          f'Is this correct? (y\\n)\n')
                    if confirm_name1 == 'n':
                        new_name_input = input('What would you like to call the anime then?\n')
                        confirm_name_of_anime(new_name_input)

            confirm_name_of_anime()

            def renaming_and_moving_files(file_location):
                if new_anime_name != Finder(original_name_of_anime).get_name():
                    file_handler = Handler(
                        location, destination, language, season, file_location, new_anime_name.capitalize()
                    )

                else:
                    file_handler = Handler(location, destination, language, season, file_location)

                file_handler.create_directory()

                name_was_renamed = file_handler.rename()

                if name_was_renamed[1] is not None:
                    print(f'File\'s name has being renamed to {name_was_renamed[1]}\n from {name_was_renamed[0]}')

                file_has_moved = file_handler.move()

                if file_has_moved:
                    print(f'File has being successfully moved')

            for name in original_name_of_anime_list:
                renaming_and_moving_files(name)

        elif users_choice == 'c':
            update_location = input('\nWhere is the files downloaded to?\n')
            update_destination = input('Where do you want to move the files to?\n')

            updated_directories = UpdateDirectoryManager(update_location, update_destination).update_directories()

            if updated_directories is not None:
                print(f'Your location has being updated to: {updated_directories[0]}\n'
                      f'Your destination has being updated to: {updated_directories[1]}')

            else:
                print('Directories has not being updated')

        elif users_choice == 'q':
            return


if __name__ == '__main__':
    main()
