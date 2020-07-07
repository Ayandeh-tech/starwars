import json
import requests
import psycopg2
import StarWarsAPI from '/StarWarsAPI'

class Database:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def _get_db_cursor(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database)
            conn.set_session(autocommit=True)
            return conn.cursor()
        except psycopg2.Error as e:
            print("Error: could not make connection to the Postgres database, {}".format(e))
            raise e

    def rebuild_tables(self):
        try:
            cur = self._get_db_cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS people (id integer PRIMARY KEY, name varchar, gender varchar, homeworld varchar);")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS starships (id integer PRIMARY KEY, name varchar, crew varchar, starship_class varchar);")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS person_starships (id serial, person_id integer REFERENCES people(id), starship_id integer REFERENCES starships(id));")
        except psycopg2.Error as e:
            print("Error: creating tables, {}".format(e))
            raise e

    def reset_tables(self):
        try:
            cur = self._get_db_cursor()
            cur.execute(
                "TRUNCATE table person_starships RESTART IDENTITY CASCADE")
            cur.execute("TRUNCATE table people RESTART IDENTITY CASCADE")
            cur.execute("TRUNCATE table starships RESTART IDENTITY CASCADE")
        except psycopg2.Error as e:
            print("Error: reseting tables, {}".format(e))
            raise e

    def insert_people(self, person_id, name, gender, homeworld):
        try:
            cur = self._get_db_cursor()
            cur.execute("INSERT INTO people (id, name, gender, homeworld) \
                     VALUES (%s, %s, %s, %s)",
                        (person_id, name, gender, homeworld))
        except psycopg2.Error as e:
            print("Error: inserting rows, {}".format(e))
            raise e

    def insert_starship(self, starship_id, name, crew, starship_class):
        try:
            cur = self._get_db_cursor()
            cur.execute("INSERT INTO starships (id, name, crew, starship_class) \
                    VALUES (%s, %s, %s, %s)",
                        (starship_id, name, crew, starship_class))
        except psycopg2.Error as e:
            print("Error: inserting rows, {}".format(e))
            raise e

    def insert_people_to_starship_relation(self, person_id, starship_id):
        try:
            cur = self._get_db_cursor()
            cur.execute("INSERT INTO person_starships (person_id, starship_id) \
                      VALUES (%s, %s)",
                        (person_id, starship_id))
        except psycopg2.Error as e:
            print("Error: inserting rows, {}".format(e))
            raise e


if __name__ == "__main__":

    # Setup database

    print("Connecting to database...")
    mydb = Database("localhost", "5490", "starwars", "stat", "starwars")

    print("Rebuilding database tables and truncating them")
    mydb.rebuild_tables()
    mydb.reset_tables()

    # Setup Star Wars API

    print("Fetching data from Star Wars API...")
    starWarsAPI = StarWarsAPI("http://swapi.dev/api")

    peopleItems = starWarsAPI.get_all_people()
    print("Fetched data for {} people".format(len(peopleItems)))

    starshipItems = starWarsAPI.get_all_starships()
    print("Fetched data for {} starships".format(len(starshipItems)))

    # Insert data to database

    print("Inserting starships to database")
    for sitem in starshipItems:
        mydb.insert_starship(
            sitem["url"].split('/')[-2], sitem["name"], sitem["crew"], sitem["starship_class"])

    print("Inserting people and relation to starships to database")
    for pitem in peopleItems:
        mydb.insert_people(
            pitem["url"].split('/')[-2], pitem["name"], pitem["gender"], pitem["homeworld"])
        for starship_url in pitem["starships"]:
            mydb.insert_people_to_starship_relation(
                pitem["url"].split('/')[-2], starship_url.split('/')[-2])
