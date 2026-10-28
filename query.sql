-- CREATE TABLE drivers (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(100) NOT NULL,
--     phone VARCHAR(20) UNIQUE
-- );

-- CREATE TABLE transport_collection (
--     id SERIAL PRIMARY KEY,
--     driver_id INTEGER NOT NULL REFERENCES drivers(id),
--     vehicle_number VARCHAR(20) NOT NULL,
--     collection_date DATE NOT NULL,
--     morning_trips INTEGER NOT NULL,
--     evening_trips INTEGER NOT NULL,
--     morning_collection NUMERIC(10, 2) NOT NULL,
--     evening_collection NUMERIC(10, 2) NOT NULL,
--     fuel_expense NUMERIC(10, 2) NOT NULL,
--     other_expense NUMERIC(10, 2) NOT NULL,
--     total_trips INTEGER NOT NULL,
--     total_collection NUMERIC(10, 2) NOT NULL,
--     total_expense NUMERIC(10, 2) NOT NULL,
--     net_collection NUMERIC(10, 2) NOT NULL
-- );



CREATE TABLE drivers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(10) UNIQUE,
    dob DATE,
    joined_date DATE NOT NULL,
    license_number VARCHAR(16) UNIQUE NOT NULL
);


CREATE TABLE transport_collection (
    id SERIAL PRIMARY KEY,
    driver_id INTEGER NOT NULL,
    vehicle_number VARCHAR(20) NOT NULL,
    collection_date DATE NOT NULL,
    morning_trips INTEGER NOT NULL,
    evening_trips INTEGER NOT NULL,
    morning_collection NUMERIC(10, 2) NOT NULL,
    evening_collection NUMERIC(10, 2) NOT NULL,
    fuel_expense NUMERIC(10, 2) NOT NULL,
    other_expense NUMERIC(10, 2) NOT NULL,
    total_trips INTEGER NOT NULL,
    total_collection NUMERIC(10, 2) NOT NULL,
    total_expense NUMERIC(10, 2) NOT NULL,
    net_collection NUMERIC(10, 2) NOT NULL,
    CONSTRAINT fk_transport_collection_driver
        FOREIGN KEY (driver_id)
        REFERENCES drivers(id)
        ON DELETE CASCADE
);



INSERT INTO drivers
    (name, phone, dob, joined_date, license_number)
VALUES
    ('Kavin', '9089786789', '2000-05-12',
     '2026-01-10', 'TN01DL1234567890'),
    ('John', '8990786789', '1999-08-21',
     '2026-02-15', 'TN02DL1234567890');


CREATE PROCEDURE delete_driver(
    driver_id_proc INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM drivers
    WHERE id = driver_id_proc;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Driver with ID % not found', driver_id_proc;
    END IF;
END;
$$;
