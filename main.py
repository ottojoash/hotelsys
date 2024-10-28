import sqlite3
import tkinter as tk
from tkinter import messagebox, Toplevel

class HotelSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("400x300")

        # Initialize database and create tables
        self.initialize_db()

        # Buttons for actions
        tk.Button(root, text="Add Room", command=self.add_room_modal).pack(pady=5)
        tk.Button(root, text="Add Guest", command=self.add_guest_modal).pack(pady=5)
        tk.Button(root, text="Create Booking", command=self.add_booking_modal).pack(pady=5)
        tk.Button(root, text="Show Rooms", command=self.show_rooms).pack(pady=5)
        tk.Button(root, text="Show Guests", command=self.show_guests).pack(pady=5)

    def initialize_db(self):
        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()
        # Create tables if they don't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT UNIQUE,
                room_type TEXT,
                price REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                contact TEXT,
                id_type TEXT,
                id_number TEXT UNIQUE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guest_id INTEGER,
                room_id INTEGER,
                check_in DATE,
                check_out DATE,
                FOREIGN KEY(guest_id) REFERENCES guests(id),
                FOREIGN KEY(room_id) REFERENCES rooms(id)
            )
        """)
        conn.commit()
        conn.close()

    def add_room_modal(self):
        modal = Toplevel(self.root)
        modal.title("Add Room")
        modal.geometry("300x250")

        tk.Label(modal, text="Room Number").pack()
        room_number_entry = tk.Entry(modal)
        room_number_entry.pack()

        tk.Label(modal, text="Room Type").pack()
        room_type_entry = tk.Entry(modal)
        room_type_entry.pack()

        tk.Label(modal, text="Price").pack()
        price_entry = tk.Entry(modal)
        price_entry.pack()

        tk.Button(modal, text="Save", command=lambda: self.add_room(room_number_entry.get(), room_type_entry.get(), price_entry.get())).pack(pady=10)

    def add_room(self, room_number, room_type, price):
        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO rooms (room_number, room_type, price) VALUES (?, ?, ?)", (room_number, room_type, price))
            conn.commit()
            messagebox.showinfo("Success", "Room added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Room number already exists!")
        finally:
            conn.close()

    def add_guest_modal(self):
        modal = Toplevel(self.root)
        modal.title("Add Guest")
        modal.geometry("300x250")

        tk.Label(modal, text="Name").pack()
        name_entry = tk.Entry(modal)
        name_entry.pack()

        tk.Label(modal, text="Contact").pack()
        contact_entry = tk.Entry(modal)
        contact_entry.pack()

        tk.Label(modal, text="ID Type").pack()
        id_type_entry = tk.Entry(modal)
        id_type_entry.pack()

        tk.Label(modal, text="ID Number").pack()
        id_number_entry = tk.Entry(modal)
        id_number_entry.pack()

        tk.Button(modal, text="Save", command=lambda: self.add_guest(name_entry.get(), contact_entry.get(), id_type_entry.get(), id_number_entry.get())).pack(pady=10)

    def add_guest(self, name, contact, id_type, id_number):
        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO guests (name, contact, id_type, id_number) VALUES (?, ?, ?, ?)", (name, contact, id_type, id_number))
            conn.commit()
            messagebox.showinfo("Success", "Guest added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Guest ID number already exists!")
        finally:
            conn.close()

    def add_booking_modal(self):
        modal = Toplevel(self.root)
        modal.title("Create Booking")
        modal.geometry("300x250")

        tk.Label(modal, text="Guest ID").pack()
        guest_id_entry = tk.Entry(modal)
        guest_id_entry.pack()

        tk.Label(modal, text="Room ID").pack()
        room_id_entry = tk.Entry(modal)
        room_id_entry.pack()

        tk.Label(modal, text="Check-in Date (YYYY-MM-DD)").pack()
        check_in_entry = tk.Entry(modal)
        check_in_entry.pack()

        tk.Label(modal, text="Check-out Date (YYYY-MM-DD)").pack()
        check_out_entry = tk.Entry(modal)
        check_out_entry.pack()

        tk.Button(modal, text="Save", command=lambda: self.create_booking(guest_id_entry.get(), room_id_entry.get(), check_in_entry.get(), check_out_entry.get())).pack(pady=10)

    def create_booking(self, guest_id, room_id, check_in, check_out):
        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO bookings (guest_id, room_id, check_in, check_out) VALUES (?, ?, ?, ?)", (guest_id, room_id, check_in, check_out))
            conn.commit()
            messagebox.showinfo("Success", "Booking created successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Invalid guest ID or room ID!")
        finally:
            conn.close()

    def show_rooms(self):
        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        conn.close()

        # Show rooms in a new modal
        modal = Toplevel(self.root)
        modal.title("Rooms Available")
        modal.geometry("400x300")

        for room in rooms:
            tk.Label(modal, text=f"Room ID: {room[0]}, Number: {room[1]}, Type: {room[2]}, Price: ${room[3]:.2f}").pack()

    def show_guests(self):
        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM guests")
        guests = cursor.fetchall()
        conn.close()

        # Show guests in a new modal
        modal = Toplevel(self.root)
        modal.title("Guests")
        modal.geometry("400x300")

        for guest in guests:
            tk.Label(modal, text=f"Guest ID: {guest[0]}, Name: {guest[1]}, Contact: {guest[2]}, ID Type: {guest[3]}, ID Number: {guest[4]}").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelSystem(root)
    root.mainloop()
