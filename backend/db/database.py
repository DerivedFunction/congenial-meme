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
            CREATE TABLE IF NOT EXISTS roster (
                rank TEXT NOT NULL,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                mi TEXT,
                edipi CHAR(10) PRIMARY KEY CHECK (LENGTH(edipi) = 10 AND edipi GLOB '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
                dor INTEGER NOT NULL,
                pmos CHAR(4) NOT NULL CHECK (LENGTH(pmos) = 4 AND pmos GLOB '[0-9][0-9][0-9][0-9]'),
                bilmos CHAR(4) NOT NULL CHECK (LENGTH(bilmos) = 4 AND bilmos GLOB '[0-9][0-9][0-9][0-9]')
            )
        ''')
        self.cursor.execute('''
           CREATE TABLE IF NOT EXISTS mos (
               bilmos CHAR(4) PRIMARY KEY CHECK (LENGTH(bilmos) = 4 AND bilmos GLOB '[0-9][0-9][0-9][0-9]'),
               desc TEXT NOT NULL,
               FOREIGN KEY (bilmos) REFERENCES roster(bilmos)
           )
        ''')
        self.conn.commit()

    def insert_user(self, rank, firstName, lastName, mi, edipi, dor, pmos, bilmos):
        """Insert a new user into the roster table."""
        self.cursor.execute('''
            INSERT INTO roster (rank, firstName, lastName, mi, edipi, dor, pmos, bilmos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (rank, firstName, lastName, mi, edipi, dor, pmos, bilmos))
        self.conn.commit()

    def update_user(self, rank, firstName, lastName, mi, edipi, dor, pmos, bilmos):
        """Update a user by edipi."""
        self.cursor.execute('''
            UPDATE roster
            SET rank = ?, firstName = ?, lastName = ?, mi = ?, dor = ?, pmos = ?, bilmos = ?
            WHERE edipi = ?
        ''', (rank, firstName, lastName, mi, dor, pmos, bilmos, edipi))
        self.conn.commit()

    def delete_user(self, edipi):
        """Delete a user by edipi."""
        self.cursor.execute('''
            DELETE FROM roster
            WHERE edipi = ?
        ''', (edipi,))
        self.conn.commit()

    def get_user_by_edipi(self, edipi):
        edipi = str(edipi)
        """Get a user by edipi, return as dictionary."""
        self.cursor.execute('''
            SELECT * FROM roster
            WHERE edipi = ?
        ''', (edipi,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_all_roster(self):
        """Get all roster, return as list of dictionaries."""
        self.cursor.execute('''
            SELECT * FROM roster
        ''')
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_all_roster_by_rank(self, rank):
        """Get all roster by rank, return as list of dictionaries."""
        self.cursor.execute('''
            SELECT * FROM roster
            WHERE rank = ?
        ''', (rank,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_all_roster_by_mos(self, bilmos):
        """Get all roster by bilmos, return as list of dictionaries."""
        bilmos = str(bilmos)
        self.cursor.execute('''
            SELECT * FROM roster
            WHERE bilmos = ?
        ''', (bilmos,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    def insert_mos_desc(self, bilmos, desc):
        """Insert a new mos description into the mos table."""
        bilmos = str(bilmos)
        self.cursor.execute('''
            INSERT INTO mos (bilmos, desc)
            VALUES (?, ?)
        ''', (bilmos, desc))
        self.conn.commit()
    def update_mos_desc(self, bilmos, desc):
        """Update a mos description by bilmos."""
        bilmos = str(bilmos)
        self.cursor('''
            UPDATE mos
            SET desc = ?
            WHERE bilmos = ?
        ''', (desc, bilmos))
        self.conn.commit()
    def delete_mos_desc(self, bilmos):
        """Delete a mos description by bilmos."""
        bilmos = str(bilmos)
        self.cursor.execute('''
            DELETE FROM mos
            WHERE bilmos = ?
        ''', (bilmos,))
        self.conn.commit()
    def get_mos_desc_by_bilmos(self, bilmos):
        """Get MOS description by bilmos, return as dictionary."""
        bilmos = str(bilmos)
        self.cursor.execute('''
            SELECT * FROM mos
            WHERE bilmos = ?
        ''', (bilmos,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    def get_all_mos_desc(self):
        """Get all mos descriptions, return as list of dictionaries."""
        self.cursor.execute('''
            SELECT * FROM mos
        ''')
        return [dict(row) for row in self.cursor.fetchall()]
    def get_all_tables(self):
        """Get all tables in the database.
            returns as an array of table names.
            {
                "tables": [
                    "table1",
                    "table2"
                ]
            }
        """
        self.cursor.execute("""SELECT name FROM sqlite_master 
                            WHERE type='table'
                            AND name NOT LIKE 'sqlite_%';
                        """)
        tables = [row[0] for row in self.cursor.fetchall()]
        return {"tables": tables}
    def run_query(self, query):
        """
        Runs any query on the database.
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
