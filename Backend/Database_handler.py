import sqlite3


class DatabaseHandler:
    def __init__(self):
        con = sqlite3.connect(r'.\Databases\database.db')
        cursor = con.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS anime_names(name text PRIMARY KEY, season integer,"
            " language text, status text, date date)"
        )
        con.commit()
        con.close()

    @staticmethod
    def add_anime(data):
        dict(data)

        con = sqlite3.connect(r'.\Databases\database.db')
        cursor = con.cursor()

        try:
            cursor.execute(
                f"INSERT INTO anime_names VALUES('{data['name']}', '{data['season']}',"
                f" '{data['language']}', '{data['status']}', '{data['date']}')"
            )
            return True

        except sqlite3.OperationalError:
            return False

        finally:
            con.commit()
            con.close()

    @staticmethod
    def get_all():
        con = sqlite3.connect(r'.\Databases\database.db')
        cursor = con.cursor()

        cursor.execute(
            "SELECT * FROM anime_names"
        )
        all_names = cursor.fetchall()

        con.commit()
        con.close()

        return all_names

    @staticmethod
    def update_entry(data_dict, name):
        dict(data_dict)
        con = sqlite3.connect(r'.\Databases\database.db')
        cursor = con.cursor()

        try:
            cursor.execute(
                f"UPDATE anime_names SET name = '{data_dict['name']}',"
                f"season = {data_dict['season']},"
                f"language = '{data_dict['language']}',"
                f"status = '{data_dict['status']}'"
                f" WHERE name = '{name}'"
            )
            return True

        except sqlite3.OperationalError:
            return False

        finally:
            con.commit()
            con.close()

    @staticmethod
    def delete_entry(name):
        con = sqlite3.connect(r'.\Databases\database.db')
        cursor = con.cursor()

        try:
            cursor.execute(
                f"DELETE FROM anime_names WHERE name = '{name}'"
            )
            return True

        except sqlite3.OperationalError:
            return False

        finally:
            con.commit()
            con.close()


test = DatabaseHandler()
to_enter = {
    'name': 'tester',
    'season': 1,
    'language': 'Dubbed',
    'status': 'complete',
    # 'date': datetime.date.today()
}
test.update_entry(to_enter, 'Tokyo Ravens')
# test.delete_entry('tester')
# test.update_entry('season', 2, 'tester')
# lists = test.get_all()
# test.add_anime(to_enter)





# Create a table in the database if it does not exist
# cursor.execute(
#     "CREATE TABLE IF NOT EXISTS anime_names(name text PRIMARY KEY, season integer, language text, status text, date date)"
# )
# con.commit()

# Insert data into the db table
# Date input must be a date object from datetime
# cursor.execute(
#     f"INSERT INTO anime_names VALUES('tester2', 1, 'dubbed', 'busy', '{datetime.date.today()}')"
# )

# con.commit()

# Update data the is in the database already
# cursor.execute(
#     "UPDATE anime_names SET status = 'done' WHERE name = 'test'"
# )
# con.commit()

# Select the data from the database
# cursor.execute(
#     "SELECT * FROM anime_names"
# )
# con.commit()

# To select specific fields from the database where the name is equal to what entered
# cursor.execute(
#     "SELECT name, season FROM anime_names WHERE name = 'test'"
# )
# con.commit()

# To get the data into a variable, use fetchall() returns list of tuple's
# cursor.execute(
#     "SELECT * FROM anime_names where name = 'test'"
# )
# data = cursor.fetchall()[0]
# print(data[0])

