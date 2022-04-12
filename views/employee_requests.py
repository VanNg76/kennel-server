import json
import sqlite3
from models import Employee, Location, Animal


def get_all_employees():
    """get all employees with location embeded"""
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT 
                e.id,
                e.name,
                e.address,
                e.location_id,
                e.animal_id,
                l.name location_name,
                l.address location_address,
                a.name animal_name,
                a.status animal_status,
                a.breed animal_breed,
                a.customer_id animal_customer_id,
                a.location_id animal_location_id
            FROM Employee e
            JOIN Location l
                ON l.id = e.location_id
            JOIN Animal a
                ON a.id = e.animal_id
        """)

        # Initialize an empty list to hold all employee representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an employee instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Employee class above.
            employee = Employee(row['id'], row['name'], row['address'],
                                row['location_id'], row['animal_id'])
            location = Location(row['location_id'], row['location_name'], row['location_address'])
            animal = Animal(row['animal_id'], row['animal_name'], row['animal_status'], row['animal_breed'],
                            row['animal_customer_id'], row['animal_location_id'])

            employee.location = location.__dict__
            employee.animal = animal.__dict__

            employees.append(employee.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(employees)


def get_single_employee(id):
    """get single customer"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
            SELECT 
                e.id,
                e.name,
                e.address,
                e.location_id,
                e.animal_id,
                l.name location_name,
                l.address location_address,
                a.name animal_name,
                a.status animal_status,
                a.breed animal_breed,
                a.customer_id animal_customer_id,
                a.location_id animal_location_id
            FROM Employee e
            JOIN Location l
                ON l.id = e.location_id
            JOIN Animal a
                ON a.id = e.animal_id
            WHERE e.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an employee instance from the current row
        employee = Employee(data['id'], data['name'], data['address'], data['location_id'], data['animal_id'])
        animal = Animal(data['animal_id'], data['animal_name'], data['animal_status'], data['animal_breed'],
                            data['animal_customer_id'], data['animal_location_id'])
        location = Location(data['location_id'], data['location_name'], data['location_address'])

        employee.animal = animal.__dict__
        employee.location = location.__dict__

        return json.dumps(employee.__dict__)

def get_employees_by_location(id):
    """Get employees by location id"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT * FROM Employee
            WHERE location_id = ?""", (id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'], row['animal_id'])
            employees.append(employee.__dict__)

    return json.dumps(employees)

def create_employee(new_employee):
    """hire new employee"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Employee
            ( name, address, location_id )
        VALUES
            ( ?, ?, ? );
        """, (new_employee['name'], new_employee['address'],
              new_employee['locationId'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_employee['id'] = id


    return json.dumps(new_employee)
