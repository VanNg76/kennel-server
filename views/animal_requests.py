import json
import sqlite3
from models import Animal, Location, Customer


def get_all_animals():
    """Get all animals"""
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.location_id,
                l.name location_name,
                l.address location_address,
                a.customer_id,
                c.name customer_name,
                c.address customer_address
            FROM Animal a
            INNER JOIN Location l
            ON l.id = a.location_id
            JOIN Customer c
            ON c.id = a.customer_id
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            animal = Animal(row['id'], row['name'], row['status'],
                            row['breed'], row['customer_id'],
                            row['location_id'])

            # Create a Location instance from the current row
            location = Location(row['location_id'], row['location_name'], row['location_address'])
            customer = Customer(row['customer_id'], row['customer_name'], row['customer_address'])

            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__
            animal.customer = customer.__dict__

            animals.append(animal.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(animals)


def get_single_animal(id):
    """Get a single animal"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.address customer_address
        FROM Animal a
        INNER JOIN Location l
            ON l.id = a.location_id
        JOIN Customer c
            ON c.id = a.customer_id
        WHERE a.id = ?""", (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['status'], data['breed'],
                        data['customer_id'], data['location_id'])

        # Create a Location instance from the current row
        location = Location(data['location_id'], data['location_name'], data['location_address'])
        customer = Customer(data['customer_id'], data['customer_name'], data['customer_address'])

        # Add the dictionary representation of the location to the animal
        animal.location = location.__dict__
        animal.customer = customer.__dict__

        return json.dumps(animal.__dict__)


def get_animals_by_location(id):
    """Get animals by location id"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT * FROM Animal
            WHERE location_id = ?""", (id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['status'], row['breed'],
                                row['customer_id'], row['location_id'])
            animals.append(animal.__dict__)

    return json.dumps(animals)

def get_animals_by_status(status):
    """Get animals by status"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT * FROM Animal
            WHERE status = ?""", (status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['status'], row['breed'],
                                row['customer_id'], row['location_id'])
            animals.append(animal.__dict__)

    return json.dumps(animals)

def delete_animal(id):
    """delete a single row"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))

def update_animal(id, new_animal):
    """update single animal"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
        SET
            name = ?,
            status = ?,
            breed = ?,
            customer_id = ?,
            location_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['status'],
              new_animal['breed'], new_animal['customerId'],
              new_animal['locationId'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def create_animal(new_animal):
    """admit new animal"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, status, breed, customer_id, location_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['status'],
              new_animal['breed'], new_animal['customerId'],
              new_animal['locationId'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id


    return json.dumps(new_animal)
