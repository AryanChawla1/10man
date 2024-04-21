# import json
import os
import psycopg2
from dotenv import load_dotenv
from player import Player
from custom_exceptions import MissingEnvVariableException, ConnectionException

load_dotenv()

PASSWORD = os.getenv('PASSWORD')  # env variable
HOST = os.getenv('HOST')
USER = os.getenv('USER')
PLAYER_TABLE = "playerinfo"  # table name


# https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
# making database class a singleton so there is only one instance of it
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=Singleton):
    create_commands = {
        "playerinfo": """
            CREATE TABLE playerinfo (
                player_id SERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                games_played INT NOT NULL,
                elo INT NOT NULL,
                roles TEXT[] NOT NULL
            )"""
    }

    def __init__(self) -> None:
        self.playerinfo_initiate = False  # check if setup for player table is completed

    def connect(self):
        # check to see if env variable is set
        if PASSWORD is None:
            raise MissingEnvVariableException(
                "Could not find password in environment variables.")
        if HOST is None:
            raise MissingEnvVariableException(
                "Could not find host in environment variables.")
        if USER is None:
            raise MissingEnvVariableException(
                "Could not find user in environment variables.")

        conn = psycopg2.connect(
            host=HOST,
            database="ten_men_db",
            user=USER,
            password=PASSWORD,
        )

        if conn is None:
            raise ConnectionException("Could not connect to Database.")
        else:
            print("Connected to Database!")
        if not self.playerinfo_initiate:
            self.conn = conn
            self.setup(PLAYER_TABLE)
        return conn

    # make sure table exists, if not create it
    def setup(self, table_name):
        if table_name not in self.create_commands:
            raise Exception("Could not find table name: " + table_name)
        cur = self.conn.cursor()
        command = """SELECT * FROM """ + table_name
        try:
            # check if table exists
            cur.execute(command)
            self.playerinfo_initiate = True
            print(PLAYER_TABLE + " table found!")
        except (Exception, psycopg2.DatabaseError):
            print(PLAYER_TABLE + " table not created, creating it now...")
            # create table
            self.conn.rollback()  # used to refresh after first query failed
            cur.execute(self.create_command[table_name])
            cur.close()
            self.conn.commit()
            self.playerinfo_initiate = True
            print(PLAYER_TABLE + " table created!")

    def create_player(self, player_data: dict):
        try:
            conn = self.connect()
            cur = conn.cursor()
            command = """INSERT INTO playerinfo(name, games_played, elo, roles) VALUES(%s, %s, %s, %s)"""
            data = (player_data["name"], player_data["games_played"],
                    player_data["elo"], player_data["roles"])
            cur.execute(command, data)
            conn.commit()
            print("Player added to Database!")
            cur.close()
            conn.close()
        except (Exception, psycopg2.DatabaseError) as e:
            print("Could not add player to Database")

    # returns Player object by filtering Database for name
    def get_player_by_name(self, name: str):
        try:
            command = """SELECT * FROM playerinfo WHERE name = '{0}'""".format(
                name)
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(command)
            player = cur.fetchone()  # id, name, games_played, elo, roles
            cur.close()
        except (Exception, psycopg2.DatabaseError) as e:
            print("Could not find player \'" + name + "\'")
        else:
            if conn is not None:
                conn.close()
            return Player(player[1], player[4], player[2], player[3])

    # update games_played and elo for player in Database
    def update_player(self, name, elo):
        try:
            command = """UPDATE playerinfo SET elo={0} WHERE name = '{1}'""".format(
                elo, name)
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(command)
            conn.commit()
            print("Updated player")
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Could not update player")


# # one time function to migrate contents from json file to database
# def migrate():
#     with open("player_info.json", "r+") as file:
#         file_data = json.load(file)
#         players = file_data["players"]
#         player_list = []
#         for player in players:
#             player_list.append(
#                 (player["name"], player["games_played"], player["elo"], player["roles"]))
#         command = "INSERT INTO playerinfo(name, games_played, elo, roles) VALUES(%s, %s, %s, %s)"
#         conn = connect()
#         cur = conn.cursor()
#         cur.executemany(command, player_list)
#         conn.commit()
#         print("migrated!")
#         cur.close()
#         conn.close()
