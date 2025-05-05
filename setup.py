import sqlite3

def setup_database(db_path="hotel.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.executescript("""
    DROP TABLE IF EXISTS Bookings;
    DROP TABLE IF EXISTS Rooms;
    DROP TABLE IF EXISTS Pricing;
    DROP TABLE IF EXISTS Customers;
    """)

    cursor.execute("""
    CREATE TABLE Customers (
        CustomerID INTEGER PRIMARY KEY,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        DOB DATE NOT NULL,
        IdentityType TEXT CHECK(IdentityType IN ('Adhar', 'PAN', 'DL')) NOT NULL,
        IdentityString TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE Pricing (
        PaymentID INTEGER PRIMARY KEY,
        PaymentType TEXT NOT NULL,
        isDone BOOLEAN NOT NULL,
        price REAL NOT NULL,
        discount REAL CHECK(discount <= 100)
    );
    """)

    cursor.execute("""
    CREATE TABLE Rooms (
        RoomID INTEGER PRIMARY KEY,
        isVacant BOOLEAN NOT NULL,
        currentStay INTEGER,
        type TEXT CHECK(type IN ('2BHK', '3BHK')) NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY(currentStay) REFERENCES Bookings(BookingsID)
    );
    """)

    cursor.execute("""
    CREATE TABLE Bookings (
        BookingsID INTEGER PRIMARY KEY,
        customerID INTEGER NOT NULL,
        bookedDate DATE NOT NULL,
        arrivalDate DATE NOT NULL,
        departureDay DATE NOT NULL,
        paymentID INTEGER NOT NULL,
        FOREIGN KEY(customerID) REFERENCES Customers(CustomerID),
        FOREIGN KEY(paymentID) REFERENCES Pricing(PaymentID)
    );
    """)

    cursor.executemany("""
    INSERT INTO Customers (CustomerID, FirstName, LastName, DOB, IdentityType, IdentityString) VALUES (?, ?, ?, ?, ?, ?);
    """, [
        (1, 'John', 'Doe', '1990-01-01', 'Adhar', '1234-5678-9012'),
        (2, 'Jane', 'Smith', '1985-05-23', 'PAN', 'ABCDE1234F'),
    ])

    cursor.executemany("""
    INSERT INTO Pricing (PaymentID, PaymentType, isDone, price, discount) VALUES (?, ?, ?, ?, ?);
    """, [
        (1, 'Credit Card', True, 1200.00, 10),
        (2, 'UPI', False, 800.00, 5),
    ])

    cursor.executemany("""
    INSERT INTO Bookings (BookingsID, customerID, bookedDate, arrivalDate, departureDay, paymentID) VALUES (?, ?, ?, ?, ?, ?);
    """, [
        (1, 1, '2025-05-01', '2025-05-05', '2025-05-10', 1),
        (2, 2, '2025-05-03', '2025-05-07', '2025-05-09', 2),
    ])

    cursor.executemany("""
    INSERT INTO Rooms (RoomID, isVacant, currentStay, type, price) VALUES (?, ?, ?, ?, ?);
    """, [
        (101, False, 1, '2BHK', 1500),
        (102, True, None, '3BHK', 2500),
    ])

    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()
