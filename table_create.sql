
PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS cookies;
DROP TABLE IF EXISTS pallets;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS inventories;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS number_of_pallets;

CREATE TABLE cookies(
    cookie_name     TEXT,
    PRIMARY KEY (cookie_name)
);

CREATE TABLE pallets(
    pallet_id       INT DEFAULT(lower(hex(randomblob(16)))),
    bake_date       DATE,
    blocked         BOOLEAN,
    cookie_name     TEXT,
    order_id        INT DEFAULT(NULL),
    PRIMARY KEY (pallet_id),
    FOREIGN KEY (cookie_name) REFERENCES cookies(cookie_name),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE orders(
    order_id        INT DEFAULT(lower(hex(randomblob(16)))),
    delivery_date   DATE,
    customer_id     INT,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE inventories(
    ingredient          TEXT,
    stock               INT DEFAULT(0),
    unit                TEXT, 
    last_delivery_date  DATE DEFAULT(NULL),
    last_delivery_quant INT DEFAULT(0),
    PRIMARY KEY (ingredient)
);

CREATE TABLE customers(
    customer_id     INT DEFAULT(lower(hex(randomblob(16)))),
    company_name    TEXT,
    address         TEXT,
    PRIMARY KEY (customer_id)
);

CREATE TABLE recipes(
    cookie_name     TEXT,
    ingredient      TEXT,
    quantity        INT,
--    unit            TEXT DEFAULT "g",
    PRIMARY KEY (ingredient, cookie_name),
    FOREIGN KEY (ingredient) REFERENCES inventories(ingredient),
    FOREIGN KEY (cookie_name) REFERENCES cookies(cookie_name)
);

CREATE TABLE number_of_pallets(
    nbr_pallets     INT,
    cookie_name     TEXT,
    order_id        INT,
    PRIMARY KEY (cookie_name, order_id),
    FOREIGN KEY (cookie_name) REFERENCES cookies(cookie_name),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
