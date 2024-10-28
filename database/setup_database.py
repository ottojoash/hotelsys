import sqlite3

def setup_database():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # Create the rooms table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number INTEGER UNIQUE NOT NULL,
            room_type TEXT NOT NULL,
            status TEXT DEFAULT 'available',
            price REAL NOT NULL
        )
    ''')

    # Create the guests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            id_type TEXT,
            id_number TEXT UNIQUE
        )
    ''')

    # Create the bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_id INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            check_in DATE,
            check_out DATE,
            FOREIGN KEY(guest_id) REFERENCES guests(id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()
