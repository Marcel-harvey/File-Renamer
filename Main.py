import sys
import datetime
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget
from Backend.Json_handler import *
from Backend.Directory_handler import *
from Backend.Database_handler import *


# Class for the main window, mainly used to select what you want to do
class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('.\\UI\\mainScreen.ui', self)

        # Button events on main window
        self.start_button.clicked.connect(self.move_to_start)
        self.view_button.clicked.connect(self.move_to_view)
        self.change_button.clicked.connect(self.move_to_change)
        self.wait_button.clicked.connect(self.move_to_wait)

    @staticmethod
    def move_to_start():
        start_process = StartProcess()
        widget.addWidget(start_process)
        widget.setCurrentIndex(widget.indexOf(start_process))

    @staticmethod
    def move_to_view():
        view_path = ViewPath()
        widget.addWidget(view_path)
        widget.setCurrentIndex(widget.indexOf(view_path))

    @staticmethod
    def move_to_change():
        change_path = ChangePath()
        widget.addWidget(change_path)
        widget.setCurrentIndex(widget.indexOf(change_path))

    @staticmethod
    def move_to_wait():
        wait_path = WaitPath()
        widget.addWidget(wait_path)
        widget.setCurrentIndex(widget.indexOf(wait_path))


# For the start window
class StartProcess(QDialog):

    data_requested = pyqtSignal(dict, name='request')

    def __init__(self):
        super(StartProcess, self).__init__()
        loadUi('.\\UI\\startProcess.ui', self)

        # To get the initial name for displaying and confirming if it is correct
        self.worker = GetOriginalNameWorker()
        self.worker_thread = QThread()

        self.worker.moveToThread(self.worker_thread)

        self.worker.finished.connect(self.worker_thread.quit)   # Ends thread
        self.worker.data.connect(self.display_on_screen)

        self.worker_thread.started.connect(self.worker.run_code)
        self.worker_thread.start()

        # Separate thread to start the renaming process
        self.process_worker = StartProcessWorker()
        self.process_thread = QThread()

        self.process_worker.finished.connect(self.worker_thread.exit)
        self.data_requested.connect(self.process_worker.run_code)
        self.process_worker.data.connect(self.log)

        self.process_worker.moveToThread(self.process_thread)

        # Hide the label and text field unless user presses No
        self.new_name_label.hide()
        self.new_name_input.hide()

        self.hidden = True

        self.start_button.clicked.connect(self.start_process)
        self.yes_button.clicked.connect(self.hide_true)
        self.no_button.clicked.connect(self.hide_false)
        self.back_button.clicked.connect(self.back_to_main)

    # For worker thread
    def display_on_screen(self, value):
        self.confirm_name_output.setText(value)

    # For process thread
    def start_process(self):
        self.process_thread.start()
        season = self.season_input.text()
        language = self.language_input.text()
        name_from_function = self.confirm_name_output.text()
        user_entered_name = self.new_name_input.text()

        try:
            is_number = int(season)
        except ValueError:
            is_number = False

        language = str(language)
        name_from_function = str(name_from_function)
        user_entered_name = str(user_entered_name)

        if season == '' or language == '':
            self.error.setText('Please enter all the fields before starting')

        elif not is_number:
            self.season_error.setText('Please enter a valid number')

        elif language.lower() != 'dubbed' and language.lower() != 'subbed':
            self.language_error.setText('Please enter a valid language')

        else:
            # For when the name from '.get_name()' method is correct
            if user_entered_name == '' and self.hidden:
                data_dict = {
                    'season': season,
                    'language': language.title(),
                    'name': name_from_function.title()
                }

                self.data_requested.emit(data_dict)

            # Fot when the name from '.get_name()' method is incorrect
            elif user_entered_name != '' and not self.hidden:
                data_dict = {
                    'season': season,
                    'language': language.title(),
                    'name': user_entered_name.title()
                }

                self.data_requested.emit(data_dict)

    def log(self, value):
        self.listWidget.addItem(value)

        if value == 'Task completed':
            self.season_input.setText('')
            self.language_input.setText('')
            self.new_name_input.setText('')

            # Hide the label again for reset
            self.new_name_label.hide()
            self.new_name_input.hide()
            self.hidden = True

    def hide_true(self):
        if not self.hidden:
            self.new_name_label.hide()
            self.new_name_input.hide()
            self.hidden = True

    def hide_false(self):
        if self.hidden:
            self.new_name_label.show()
            self.new_name_input.show()
            self.hidden = False

    def back_to_main(self):
        # Close the thread, because they can still run when you do nothing in the window
        self.worker_thread.quit()
        self.process_thread.quit()
        widget.removeWidget(widget.currentWidget())


# For the View selected paths window
class ViewPath(QDialog):
    def __init__(self):
        super(ViewPath, self).__init__()
        loadUi('.\\UI\\viewSelectedPathsScreen.ui', self)

        self.worker = GetDirectoryWorker()
        self.worker_thread = QThread()

        self.worker.moveToThread(self.worker_thread)

        self.worker.finished.connect(self.worker_thread.quit)   # Ends thread
        self.worker.data.connect(self.display_on_screen)

        self.worker_thread.started.connect(self.worker.run_code)
        self.worker_thread.start()

        self.back_button.clicked.connect(self.back_to_main)

    def display_on_screen(self, values):
        self.location_output.setText(values['location'].title())
        self.destination_output.setText(values['destination'].title())

    @staticmethod
    def back_to_main():
        # Remove the widget from the stack, to save memory, when going back to main screen
        widget.removeWidget(widget.currentWidget())


# For the Change paths window
class ChangePath(QDialog):

    data_requested = pyqtSignal(str, str, name='data')

    def __init__(self):
        super(ChangePath, self).__init__()
        loadUi('.\\UI\\changeSelectedPathsScreen.ui', self)

        self.worker = ChangePathWorker()
        self.worker_thread = QThread()

        self.worker.moveToThread(self.worker_thread)

        self.worker.finished.connect(self.worker_thread.quit)  # Ends thread
        self.data_requested.connect(self.worker.run_code)
        self.worker.data.connect(self.update_window)

        self.submit_button.clicked.connect(self.submitted)
        self.back_button.clicked.connect(self.back_to_main)

    def submitted(self):
        self.worker_thread.start()

        # Get the text that was in the input fields when button is clicked
        location = self.location_input.text()
        destination = self.destination_input.text()

        self.data_requested.emit(location.title(), destination.title())

    def update_window(self, val):
        if val is not None:
            self.update_label.setText('Successfully Updated New Paths')
            self.location_input.setText('')
            self.destination_input.setText('')

    @staticmethod
    def back_to_main():
        widget.removeWidget(widget.currentWidget())


# For the View Wait List window
class WaitPath(QDialog):

    date_requested = pyqtSignal(dict, name='values')
    delete_requested = pyqtSignal(str, name='values')
    update_requested = pyqtSignal(dict, str, name='values')

    def __init__(self):
        super(WaitPath, self).__init__()
        loadUi('.\\UI\\viewWaitList.ui', self)

        # Start the thread when window is opened
        # Thread for displaying everything on the listWidget
        self.worker = GetDataFromDatabaseWorker()
        self.worker_thread = QThread()

        self.worker.finished.connect(self.worker_thread.quit)   # Ends thread
        self.worker.data.connect(self.display_on_screen)

        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run_code)
        self.worker_thread.start()

        # Separate thread for adding a new entry to the database
        self.add_worker = AddToDatabaseWorker()
        self.add_worker_thread = QThread()

        self.add_worker.finished.connect(self.add_worker_thread.quit)   # Ends thread
        self.date_requested.connect(self.add_worker.run_code)
        self.add_worker.data.connect(self.show_message)

        self.add_worker.moveToThread(self.add_worker_thread)

        # Separate thread for deleting objects from the database
        self.delete_worker = DeleteFromDatabaseWorker()
        self.delete_worker_thread = QThread()

        self.delete_worker.finished.connect(self.delete_worker_thread.quit)     # Ends thread
        self.delete_requested.connect(self.delete_worker.run_code)
        self.delete_worker.data.connect(self.show_message)

        self.delete_worker.moveToThread(self.delete_worker_thread)

        # Separate thread for updating the database
        self.update_worker = UpdateDatabaseWorker()
        self.update_worker_thread = QThread()

        self.update_worker.finished.connect(self.update_worker_thread.exit)
        self.update_requested.connect(self.update_worker.run_code)
        self.update_worker.data.connect(self.show_message)

        self.update_worker.moveToThread(self.update_worker_thread)

        # Event trigger for the QWidgetList
        self.listWidget.itemDoubleClicked.connect(self.get_item)

        # Hide all the required items so that only the needed items can be shown when required
        self.update_button.hide()
        self.delete_button.hide()
        self.add_button_2.hide()

        self.name_checkbox.hide()
        self.name_input.hide()

        self.season_checkbox.hide()
        self.season_input.hide()

        self.language_checkbox.hide()
        self.language_input.hide()

        self.status_checkbox.hide()
        self.status_input.hide()

        self.hidden = True
        self.hide_add = True

        self.add_button.clicked.connect(self.show_fields_for_add)
        self.add_button_2.clicked.connect(self.add_new)
        self.delete_button.clicked.connect(self.delete_item)
        self.update_button.clicked.connect(self.update_database)
        self.back_button.clicked.connect(self.back_to_main)

    def display_on_screen(self, values):
        for name in values:
            self.listWidget.addItem(f'------ ENTRY ------\n'
                                    f'Name:\t{name[0].title()}\n'
                                    f'Season:\t{name[1]}\n'
                                    f'Language:\t{name[2].title()}\n'
                                    f'Status:\t{name[3].title()}\n'
                                    f'Date added:\t{name[4]}\n')

    # For adding new entries to database
    def add_new(self):
        self.add_worker_thread.start()
        # Get the data in the all the text fields
        data = {
            'name': str(self.name_input.text()).title(),
            'season': self.season_input.text(),
            'language': str(self.language_input.text()).title(),
            'status': str(self.status_input.text()).title(),
            'date': datetime.date.today()
        }

        self.date_requested.emit(data)

    def show_fields_for_add(self):
        # Show all the required items and hide the update and delete buttons
        if self.hide_add:
            self.add_button_2.show()
            self.update_button.hide()
            self.delete_button.hide()

            self.hidden = True
            self.hide_add = False

        self.name_checkbox.show()
        self.name_input.show()

        self.season_checkbox.show()
        self.season_input.show()

        self.language_checkbox.show()
        self.language_input.show()

        self.status_checkbox.show()
        self.status_input.show()

    # Used for when delete or update needs to happen
    def get_item(self, data):
        item = data.text()
        item = str(item)
        item_list = re.split(':\t|\n', item)

        # Show all the required items and hide the add button
        if self.hidden:
            self.update_button.show()
            self.delete_button.show()
            self.add_button_2.hide()

            self.hidden = False
            self.hide_add = True

        self.name_checkbox.show()
        self.name_input.show()
        self.name_input.setText(item_list[2].title())

        self.season_checkbox.show()
        self.season_input.show()
        self.season_input.setText(item_list[4])

        self.language_checkbox.show()
        self.language_input.show()
        self.language_input.setText(item_list[6].title())

        self.status_checkbox.show()
        self.status_input.show()
        self.status_input.setText(item_list[8].title())

    # For deleting items from the database
    def delete_item(self):
        self.delete_worker_thread.start()
        name = self.name_input.text()

        self.delete_requested.emit(name)

    # For updating items in the database
    def update_database(self):
        self.update_worker_thread.start()

        item = self.listWidget.currentItem().text()
        item_list = re.split(':\t|\n', item)
        name = item_list[2]

        data = {
            'name': str(self.name_input.text()).title(),
            'season': self.season_input.text(),
            'language': str(self.language_input.text()).title(),
            'status': str(self.status_input.text()).title()
        }

        self.update_requested.emit(data, name)

    def show_message(self, display):
        # Generic for multiple uses
        self.message_box.setText(display)
        self.listWidget.clear()
        self.name_input.setText('')
        self.season_input.setText('')
        self.language_input.setText('')
        self.status_input.setText('')
        self.worker_thread.start()

    @staticmethod
    def back_to_main():
        widget.removeWidget(widget.currentWidget())


# All the Thread workers for QThread
# Class to get the original name
class GetOriginalNameWorker(QObject):

    finished = pyqtSignal(name='exit')
    data = pyqtSignal(str, name='value')

    def __init__(self):
        super(GetOriginalNameWorker, self).__init__()

    def run_code(self):
        location = GetDirectoryManager().get_location()
        anime_list = GetDirectoryPath(location).get_path()

        if len(anime_list) == 0:
            self.finished.emit()
        else:
            new_name = Finder(anime_list[0]).get_name()
            self.data.emit(new_name)
        self.finished.emit()
        print(f'Find name thread id: {int(self.thread().currentThreadId())}')


# Class for the entire renaming and moving process
class StartProcessWorker(QObject):

    finished = pyqtSignal(name='exit')
    data = pyqtSignal(str, name='value')

    def __init__(self):
        super(StartProcessWorker, self).__init__()

    @pyqtSlot(dict)
    def run_code(self, data_dict):
        location = GetDirectoryManager().get_location()
        destination = GetDirectoryManager().get_destination()
        anime_list = GetDirectoryPath(location).get_path()
        confirm_name = Finder(anime_list[0]).get_name()

        if len(anime_list) == 0:
            self.data.emit('No Anime found')
            self.finished.emit()

        else:
            if confirm_name == data_dict['name']:
                for anime_name in anime_list:
                    file_handler = Handler(
                        location, destination, data_dict['language'], data_dict['season'], anime_name
                    )
                    file_handler.create_directory()

                    self.data.emit('------ Renaming the file ------')
                    was_renamed = file_handler.rename()

                    if was_renamed[1] is not None:
                        self.data.emit(f'File was renamed to {was_renamed[1]}')

                    self.data.emit('------ Moving file ------')
                    file_moved = file_handler.move()

                    if file_moved:
                        self.data.emit('File has being moved to new directory\n')

            else:
                for anime_name in anime_list:
                    file_handler = Handler(
                        location, destination, data_dict['language'], data_dict['season'], anime_name, data_dict['name']
                    )
                    file_handler.create_directory()

                    self.data.emit('------ Renaming the file ------')
                    was_renamed = file_handler.rename()

                    if was_renamed[1] is not None:
                        self.data.emit(f'File was renamed to {was_renamed[1]}')

                    self.data.emit('------ Moving file ------')
                    file_moved = file_handler.move()

                    if file_moved:
                        self.data.emit('File has being moved to new directory\n')

        self.data.emit('Task completed')
        self.finished.emit()
        print(f'Start process thread id: {int(self.thread().currentThreadId())}')


# Class to get the chosen directories
class GetDirectoryWorker(QObject):

    finished = pyqtSignal(name='exit')
    data = pyqtSignal(dict, name='value')
    
    def __init__(self):
        super(GetDirectoryWorker, self).__init__()

    def run_code(self):
        location = GetDirectoryManager().get_location()
        destination = GetDirectoryManager().get_destination()
        print(f'Get Directories thread id: {int(self.thread().currentThreadId())}')

        self.data.emit({'location': location, 'destination': destination})
        self.finished.emit()


# Class for changing the directories
class ChangePathWorker(QObject):

    finished = pyqtSignal(name='exit')
    data = pyqtSignal(list, name='value')

    def __init__(self):
        super(ChangePathWorker, self).__init__()

    def run_code(self, location, destination):
        update_directories = UpdateDirectoryManager(location, destination).update_directories()
        print(f'Update thread id: {int(self.thread().currentThreadId())}')

        self.data.emit(update_directories)
        self.finished.emit()    # For when thread is finished


# Wait list section/Database section
# Get all the data in the database
class GetDataFromDatabaseWorker(QObject):

    finished = pyqtSignal(name='exit')
    data = pyqtSignal(list, name='value')

    def __init__(self):
        super(GetDataFromDatabaseWorker, self).__init__()

    def run_code(self):
        name_list = DatabaseHandler().get_all()

        self.data.emit(name_list)
        self.finished.emit()
        print(f'Get all the database data thread id: {int(self.thread().currentThreadId())}')


# Add a new entry to the database
class AddToDatabaseWorker(QObject):

    finished = pyqtSignal(name='exit')
    data = pyqtSignal(str, name='data')

    def __init__(self):
        super(AddToDatabaseWorker, self).__init__()

    def run_code(self, data_dict):
        completed = DatabaseHandler().add_anime(data_dict)

        if completed:
            self.data.emit('Successfully added the anime to the database')

        else:
            self.data.emit('An error has occurred while adding the anime to the database')

        self.finished.emit()
        print(f'Add to database thread id: {int(self.thread().currentThreadId())}')


class DeleteFromDatabaseWorker(QObject):

    finished = pyqtSignal(name='exit')
    data = pyqtSignal(str, name='value')

    def __init__(self):
        super(DeleteFromDatabaseWorker, self).__init__()

    def run_code(self, name):
        is_deleted = DatabaseHandler().delete_entry(name)

        if is_deleted:
            self.data.emit('Anime has being deleted from the database')

        else:
            self.data.emit('There was an error deleting your item from the database')

        self.finished.emit()
        print(f'Delete from database thread id: {int(self.thread().currentThreadId())}')


class UpdateDatabaseWorker(QObject):

    finished = pyqtSignal(name='exit')
    data = pyqtSignal(str, name='data')

    def __init__(self):
        super(UpdateDatabaseWorker, self).__init__()

    def run_code(self, data_dict, name):
        is_updated = DatabaseHandler().update_entry(data_dict, name)

        if is_updated:
            self.data.emit('The database has being successfully updated')
        else:
            self.data.emit('The update was not successful')

        self.finished.emit()
        print(f'Update database thread id: {int(self.thread().currentThreadId())}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()

    widget = QStackedWidget()
    widget.addWidget(main_window)
    widget.setFixedHeight(500)
    widget.setFixedWidth(900)
    widget.show()

    sys.exit(app.exec_())

# https://www.youtube.com/watch?v=Hwk242UMFR8
# The one that helped
# https://www.youtube.com/watch?v=UNMqx3TUuYI
# 40minutes, was last watch
# List widget extras
# https://www.youtube.com/watch?v=7hbL0ztIYCg
# Check box select and deselect with events attached
# https://www.geeksforgeeks.org/pyqt5-selecting-any-one-check-box-among-group-of-check-boxes/
