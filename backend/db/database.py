import sqlite3

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Create and return a database connection."""
        self.conn = sqlite3.connect('database.db')
        self.conn.row_factory = sqlite3.Row  # Allows accessing rows as dictionaries
        self.cursor = self.conn.cursor()
        self.create_table()

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def create_table(self):
        """Create tables if they don't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rank TEXT NOT NULL,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                mi TEXT,
                edipi CHAR(10) NOT NULL UNIQUE CHECK (LENGTH(edipi) = 10 AND edipi GLOB '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
                dor INTEGER NOT NULL,
                pmos CHAR(4) NOT NULL CHECK (LENGTH(pmos) = 4 AND pmos GLOB '[0-9][0-9][0-9][0-9]'),
                bilmos CHAR(4) NOT NULL CHECK (LENGTH(bilmos) = 4 AND bilmos GLOB '[0-9][0-9][0-9][0-9]')
            )
        ''')
        self.cursor.execute('''
           CREATE TABLE IF NOT EXISTS mosdesc (
               bilmos CHAR(4) PRIMARY KEY CHECK (LENGTH(bilmos) = 4 AND bilmos GLOB '[0-9][0-9][0-9][0-9]'),
               desc TEXT NOT NULL,
               FOREIGN KEY (bilmos) REFERENCES users(bilmos)
           )
        ''')
        self.conn.commit()

    def insert_user(self, rank, firstName, lastName, mi, edipi, dor, pmos, bilmos):
        """Insert a new user into the users table."""
        self.cursor.execute('''
            INSERT INTO users (rank, firstName, lastName, mi, edipi, dor, pmos, bilmos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (rank, firstName, lastName, mi, edipi, dor, pmos, bilmos))
        self.conn.commit()

    def update_user(self, rank, firstName, lastName, mi, edipi, dor, pmos, bilmos):
        """Update a user by edipi."""
        self.cursor.execute('''
            UPDATE users
            SET rank = ?, firstName = ?, lastName = ?, mi = ?, dor = ?, pmos = ?, bilmos = ?
            WHERE edipi = ?
        ''', (rank, firstName, lastName, mi, dor, pmos, bilmos, edipi))
        self.conn.commit()

    def delete_user(self, edipi):
        """Delete a user by edipi."""
        self.cursor.execute('''
            DELETE FROM users
            WHERE edipi = ?
        ''', (edipi,))
        self.conn.commit()

    def get_user_by_edipi(self, edipi):
        """Get a user by edipi, return as dictionary."""
        self.cursor.execute('''
            SELECT * FROM users
            WHERE edipi = ?
        ''', (edipi,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_all_users(self):
        """Get all users, return as list of dictionaries."""
        self.cursor.execute('''
            SELECT * FROM users
        ''')
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_all_users_by_rank(self, rank):
        """Get all users by rank, return as list of dictionaries."""
        self.cursor.execute('''
            SELECT * FROM users
            WHERE rank = ?
        ''', (rank,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_all_users_by_mos(self, bilmos):
        """Get all users by bilmos, return as list of dictionaries."""
        self.cursor.execute('''
            SELECT * FROM users
            WHERE bilmos = ?
        ''', (bilmos,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    def insert_mos_desc(self, bilmos, desc):
        """Insert a new mos description into the mosdesc table."""
        self.cursor.execute('''
            INSERT INTO mosdesc (bilmos, desc)
            VALUES (?, ?)
        ''', (bilmos, desc))
        self.conn.commit()
    def update_mos_desc(self, bilmos, desc):
        """Update a mos description by bilmos."""
        self.cursor('''
            UPDATE mosdesc
            SET desc = ?
            WHERE bilmos = ?
        ''', (desc, bilmos))
        self.conn.commit()
    def delete_mos_desc(self, bilmos):
        """Delete a mos description by bilmos."""
        self.cursor.execute('''
            DELETE FROM mosdesc
            WHERE bilmos = ?
        ''', (bilmos,))
        self.conn.commit()
    def get_mos_desc_by_bilmos(self, bilmos):
        """Get a mos description by bilmos, return as dictionary."""
        self.cursor.execute('''
            SELECT * FROM mosdesc
            WHERE bilmos = ?
        ''', (bilmos,))
        return dict(self.cursor.fetchone()) if self.cursor.fetchone() else None
    def get_all_mos_desc(self):
        """Get all mos descriptions, return as list of dictionaries."""
        self.cursor.execute('''
            SELECT * FROM mosdesc
        ''')
        return [dict(row) for row in self.cursor.fetchall()]