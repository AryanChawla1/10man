# import json
import os
import psycopg2

from player import Player

PASSWORD = os.environ.get('PASSWORD')  # env variable
PLAYER_TABLE = "playerinfo"  # table name


# make sure table exists, if not create it
def setup(conn):
    cur = conn.cursor()
    command = "SELECT * FROM " + PLAYER_TABLE
    try:
        # check if table exists
        cur.execute(command)
        print(PLAYER_TABLE + " table found!")
    except (Exception, psycopg2.DatabaseError):
        print(PLAYER_TABLE + " table not created, creating it now...")
        # create table
        create_command = """
         CREATE TABLE playerinfo (
            player_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            games_played INT NOT NULL,
            elo INT NOT NULL,
            roles TEXT[] NOT NULL
        )"""
        conn.rollback()  # used to refresh after first query failed
        cur.execute(create_command)
        cur.close()
        conn.commit()
        print(PLAYER_TABLE + " table created!")


def connect():
    # check to see if env variable is set
    if PASSWORD is None:
        raise Exception("Could not find password in environment variable.")

    conn = psycopg2.connect(
        host="10.144.0.1",
        database="ten_men_db",
        user="postgres",
        password=PASSWORD,
    )

    if conn is None:
        raise Exception("Could not connect to database.")
    else:
        print("Connected to Database!")

    setup(conn)
    return conn


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


def create_player(player_data: dict):
    try:
        conn = connect()
        cur = conn.cursor()
        command = "INSERT INTO playerinfo(name, games_played, elo, roles) VALUES(%s, %s, %s, %s)"
        data = (player_data["name"], player_data["games_played"],
                player_data["elo"], player_data["roles"])
        cur.execute(command, data)
        conn.commit()
        print("Player added to Database!")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print("Could not add player to Database")
    finally:
        if conn is not None:
            conn.close()


# returns Player object by filtering Database for name
def get_player_by_name(name: str):
    try:
        command = """SELECT * FROM playerinfo WHERE name = '{0}'""".format(
            name)
        conn = connect()
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
    finally:
        if conn is not None:
            conn.close()


# update games_played and elo for player in Database
def update_player(name, elo):
    try:
        command = """UPDATE playerinfo SET elo={0} WHERE name = '{1}'""".format(
            elo, name)
        conn = connect()
        cur = conn.cursor()
        cur.execute(command)
        conn.commit()
        print("Updated player")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Could not update player")
    finally:
        if conn is not None:
            conn.close()
