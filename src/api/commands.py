
import click
import requests
from api.models import Planet, db, User, Person

"""
In this file, you can add as many commands as you want using the @app.cli.command decorator
Flask commands are usefull to run cronjobs or tasks outside of the API but sill in integration 
with youy database, for example: Import the price of bitcoin every night as 12am
"""
def setup_commands(app):
    
    """ 
    This is an example command "insert-test-users" that you can run from the command line
    by typing: $ flask insert-test-users 5
    Note: 5 is the number of users to add
    """
    @app.cli.command("insert-test-users") # name of our command
    @click.argument("count") # argument of out command
    def insert_test_data(count):
        print("Creating test users")
        for x in range(1, int(count) + 1):
            user = User()
            user.email = "test_user" + str(x) + "@test.com"
            user.set_password("123456")
            user.is_active = True
            db.session.add(user)
            db.session.commit()
            print("User: ", user.email, " created.")

        print("All test users created")


    @app.cli.command("insert-people") # name of our command
    def insert_people_data():
        print("Creating stars wars people")
        people = requests.get(url="https://swapi.dev/api/people").json().get("results")
        for p in people:
            person = Person()
            person.name = p["name"]
            person.height = p["height"]
            person.mass = p["mass"]
            db.session.add(person)
            db.session.commit()
            print("Person: ", person.name, " created.")

        print("All persons created")


    @app.cli.command("insert-planets") # name of our command
    def insert_planets_data():
        print("Creating stars wars planets")
        planets = requests.get(url="https://swapi.dev/api/planets").json().get("results")
        for p in planets:
            planet = Planet()
            planet.name = p["name"]
            planet.climate = p["climate"]
            planet.gravity = p["gravity"]
            planet.population = p["population"]
            db.session.add(planet)
            db.session.commit()
            print("Person: ", planet.name, " created.")

        print("All planets created")

        ### Insert the code to populate others tables if needed