from bottle import get, post, run, request, response
import sqlite3
import json
import hashlib
import datetime

conn = sqlite3.connect('database.db')

@get('/ping')
def ping():
    return 'pong \n'

@post('/reset')
def reset_db():
    response.content_type = 'application/json'
    c = conn.cursor()
    _run_command_file('table_create.sql')
    # Populating customers
    c.execute(
        """
        INSERT
        INTO customers(company_name, address)
        VALUES  ("Finkakor AB", "Helsingborg"),
                ("Småbröd AB", "Malmö"),
                ("Kaffebröd AB", "Landskrona"),
                ("Bjudkakor AB", "Ystad"),
                ("Kalaskakor AB", "Trelleborg"),
                ("Partykakor AB", "Kristianstad"),
                ("Gästkakor AB", "Hässleholm"),
                ("Skånekakor AB", "Perstorp")
        """
    )
    conn.commit()
    # Populating cookies
    c.execute(
        """
        INSERT
        INTO cookies(cookie_name)
        VALUES  ("Nut ring"),
                ("Nut cookie"),
                ("Amneris"),
                ("Tango"),
                ("Almond delight"),
                ("Berliner")
        """
    )
    conn.commit()
    # Populating ingredients (inventory in sql)
    c.execute(
        """
        INSERT
        INTO    inventories(ingredient, stock, unit)
        VALUES  ("Flour", "100000", "g"),
                ("Butter", "100000", "g"),
                ("Icing sugar", "100000", "g"),
                ("Roasted, chopped nuts", "100000", "g"),
                ("Fine-ground nuts", "100000", "g"),
                ("Ground, roasted nuts", "100000", "g"),
                ("Bread crumbs", "100000", "g"),
                ("Sugar", "100000", "g"),
                ("Egg whites", "100000", "ml"),
                ("Chocolate", "100000", "g"),
                ("Marzipan", "100000", "g"),
                ("Eggs", "100000", "g"),
                ("Potato starch", "100000", "g"),
                ("Wheat flour", "100000", "g"),
                ("Sodium bicarbonate", "100000", "g"),
                ("Vanilla", "100000", "g"),
                ("Chopped almonds", "100000", "g"),
                ("Cinnamon", "100000", "g"),
                ("Vanilla sugar", "100000", "g")
        """
    )
    conn.commit()
    # Populating recipes
    c.execute(
        """
        INSERT
        INTO recipes(cookie_name, ingredient, quantity)
        VALUES  ("Nut ring", "Flour", "450"),
                ("Nut ring", "Butter", "450"),
                ("Nut ring", "Icing sugar", "190"),
                ("Nut ring", "Roasted, chopped nuts", "225"),
                ("Nut cookie", "Fine-ground nuts", "750"),
                ("Nut cookie", "Ground, roasted nuts", "625"),
                ("Nut cookie", "Bread crumbs", "125"),
                ("Nut cookie", "Sugar", "375"),
                ("Nut cookie", "Egg whites", "350"),
                ("Nut cookie", "Chocolate", "50"),
                ("Amneris", "Marzipan", "750"),
                ("Amneris", "Butter", "250"),
                ("Amneris", "Eggs", "250"),
                ("Amneris", "Potato starch", "25"),
                ("Amneris", "Wheat flour", "25"),
                ("Tango", "Butter", "200"),
                ("Tango", "Sugar", "250"),
                ("Tango", "Flour", "300"),
                ("Tango", "Sodium bicarbonate", "4"),
                ("Tango", "Vanilla", "2"),
                ("Almond delight", "Butter", "400"),
                ("Almond delight", "Sugar", "270"),
                ("Almond delight", "Chopped almonds", "279"),
                ("Almond delight", "Flour", "400"),
                ("Almond delight", "Cinnamon", "10"),
                ("Berliner", "Flour", "350"),
                ("Berliner", "Butter", "250"),
                ("Berliner", "Icing sugar", "100"),
                ("Berliner", "Eggs", "50"),
                ("Berliner", "Vanilla sugar", "5"),
                ("Berliner", "Chocolate", "50")
        """
    )
    conn.commit()
    # Response OK
    response.status = 200
    return json.dumps({"status": "ok"}, indent=4)

@get('/customers')
def get_customers():
    response.content_type = 'application/json'
    c = conn.cursor()
    query = """
            SELECT company_name, address
            FROM customers
            """
    c.execute(query)
    # Go to the cursor and get the right table
    s = [{"name": company_name, "address": address}
        for (company_name, address) in c]
    response.status = 200
    return json.dumps({"customers" : s}, indent = 4)

@get('/recipes')
def get_recipes():
    response.content_type = 'application/json'
    c = conn.cursor()
    query = """
            SELECT cookie_name, ingredient, quantity, unit
            FROM recipes
            INNER JOIN inventories
            USING(ingredient)
            ORDER BY(cookie_name)
            """
    c.execute(query)
    s = [{"cookie": cookie_name, "ingredient": ingredient,
        "quantity": quantity, "unit": unit}
        for (cookie_name, ingredient, quantity, unit) in c]
    response.status = 200
    return json.dumps({"recipes": s}, indent = 4)

@get('/ingredients')
def get_ingredients():
    response.content_type = 'application/json'
    c = conn.cursor()
    query = """
            SELECT ingredient, stock, unit
            FROM inventories
            """
    c.execute(query)
    s = [{"name": ingredient, "quantity": stock, "unit": unit}
        for (ingredient, stock, unit) in c]
    response.status = 200
    return json.dumps({"ingredients" : s}, indent = 4)

@get('/pallets')
def get_pallets():
    response.content_type = 'application/json'
    c = conn.cursor()
    query = """
            SELECT pallet_id, cookie_name, bake_date, company_name, blocked
            FROM pallets
            LEFT OUTER JOIN orders
            USING (order_id)
            LEFT OUTER JOIN customers
            USING (customer_id)

            """
    c.execute(query)
    s = [{"id": pallet_id, "cookie": cookie_name, "productionDate": bake_date, "customer": company_name, "blocked": blocked}
        for (pallet_id, cookie_name, bake_date, company_name, blocked) in c]
    response.status = 200
    return json.dumps({"pallets" : s}, indent = 4)

@post('/pallets')
def put_pallets():
    response.content_type = 'application/json'
    c = conn.cursor()
    cookie = request.query.cookie
    print("URL input är: {}".format(cookie))
    query = """
            SELECT cookie_name, ingredient, stock, quantity
            FROM cookies
            INNER JOIN recipes
            USING(cookie_name)
            INNER JOIN inventories
            USING(ingredient)
            WHERE cookie_name = ?
            """

    c.execute(query, [cookie])

    s = [{"name": cookie_name, "ingredient": ingredient, "stock": stock, "quantity": quantity}
        for (cookie_name, ingredient, stock, quantity) in c]
    # Each pallet contains 5400 cookies. Quantity Stock must be 54 times Quantity
    INGREDIENT_FACTOR = 54
    if not s:
        return json.dumps({"status": "no such cookie"}, indent = 4)

    for element in s:
        quantity_needed = element["quantity"] * INGREDIENT_FACTOR
        if element["stock"] < quantity_needed:
            print("AVBRYTS")
            return json.dumps({"status": "not enough ingredients"})

    for element in s:
        quantity_needed = element["quantity"] * INGREDIENT_FACTOR
        query = """
                UPDATE inventories
                SET stock = stock - ?
                WHERE ingredient = ?
                """
        values = [quantity_needed, element['ingredient']]
        c.execute(query, values)
            
    conn.commit()            
    query = """
            INSERT
            INTO pallets(bake_date, blocked, cookie_name)
            VALUES(?, ?, ?)
            """
    values = [datetime.datetime.now(), False, cookie]
    c.execute(query, values)
    conn.commit()
    query = """
            SELECT pallet_id
            FROM pallets
            WHERE rowid = last_insert_rowid()
            """
    c.execute(query)
    pallet_id = c.fetchall()[0]
    return json.dumps({"status": "ok", "id": pallet_id[0]}, indent=4)

@get('/cookies')
def get_cookies():
    response.content_type = 'application/json'
    c = conn.cursor()
    query = """
            SELECT cookie_name
            FROM cookies
            ORDER BY cookie_name
            """
    c.execute(query)
    s = [{ "name": cookie_name[0]}
        for cookie_name in c]
    response.status = 200
    return json.dumps({"cookies" : s}, indent=4)

@post('/block/<cookie_name>/<from_date>/<to_date>')
def block_pallet(cookie_name, from_date, to_date):
    response.content_type = 'application/json'
    c = conn.cursor()

    query = """
            UPDATE pallets
            SET blocked = TRUE
            WHERE DATE(bake_date) = ? AND cookie_name = ?
            """
    c.execute(query, [from_date, cookie_name])
    conn.commit()

    return json.dumps({"status" : "ok"}, indent=4)

@post('/unblock/<cookie_name>/<from_date>/<to_date>')
def unblock_pallet(cookie_name, from_date, to_date):
    response.content_type = 'application/json'
    c = conn.cursor()

    query = """
            UPDATE pallets
            SET blocked = FALSE
            WHERE DATE(bake_date) = ? AND cookie_name = ?
            """

    c.execute(query, [from_date, cookie_name])
    conn.commit()

    return json.dumps({"status" : "ok"}, indent=4)

def _run_command_file(filename, seperator = ';'):
    '''Runs all commmands in the file with the specified seperator,
    where seperator is ";" as default'''

    commands = open(filename, 'r').read().split(seperator)
    for command in commands:
        try:
            conn.execute(command)
        except:
            print("Except in 'run_command_file'. Command not valid. Command is {}".format(command))

run(host='localhost', port=8888)
