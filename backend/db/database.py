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
                RANK TEXT NOT NULL,
                FIRSTNAME TEXT NOT NULL,
                LASTNAME TEXT NOT NULL,
                MI TEXT,
                EDIPI CHAR(10) PRIMARY KEY CHECK (LENGTH(EDIPI) = 10 AND EDIPI GLOB '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
                DOR INTEGER NOT NULL,
                PMOS CHAR(4) NOT NULL CHECK (LENGTH(PMOS) = 4 AND PMOS GLOB '[0-9][0-9][0-9][0-9]'),
                BILMOS CHAR(4) NOT NULL CHECK (LENGTH(BILMOS) = 4 AND BILMOS GLOB '[0-9][0-9][0-9][0-9]')
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mos (
                BILMOS CHAR(4) PRIMARY KEY CHECK (LENGTH(BILMOS) = 4 AND BILMOS GLOB '[0-9][0-9][0-9][0-9]'),
                DESCRIPTION TEXT NOT NULL,
                FOREIGN KEY (BILMOS) REFERENCES roster(BILMOS)
            )
        ''')
        self.conn.commit()

    def insert_user(self, rank, firstname, lastname, mi, edipi, dor, pmos, bilmos):
        """Insert a new user into the roster table."""
        self.cursor.execute('''
            INSERT INTO roster (RANK, FIRSTNAME, LASTNAME, MI, EDIPI, DOR, PMOS, BILMOS)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (rank, firstname, lastname, mi, edipi, dor, pmos, bilmos))
        self.conn.commit()

    def update_user(self, rank, firstname, lastname, mi, edipi, dor, pmos, bilmos):
        """Update a user by EDIPI."""
        self.cursor.execute('''
            UPDATE roster
            SET RANK = ?, FIRSTNAME = ?, LASTNAME = ?, MI = ?, DOR = ?, PMOS = ?, BILMOS = ?
            WHERE EDIPI = ?
        ''', (rank, firstname, lastname, mi, dor, pmos, bilmos, edipi))
        self.conn.commit()

    def delete_user(self, edipi):
        """Delete a user by EDIPI."""
        self.cursor.execute('''
            DELETE FROM roster
            WHERE EDIPI = ?
        ''', (edipi,))
        self.conn.commit()

    def get_user_by_edipi(self, edipi):
        """Get a user by EDIPI, return as dictionary."""
        edipi = str(edipi)
        self.cursor.execute('''
            SELECT * FROM roster
            WHERE EDIPI = ?
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
        """Get all roster by RANK, return as list of dictionaries."""
        self.cursor.execute('''
            SELECT * FROM roster
            WHERE RANK = ?
        ''', (rank,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_all_roster_by_mos(self, bilmos):
        """Get all roster by BILMOS, return as list of dictionaries."""
        bilmos = str(bilmos)
        self.cursor.execute('''
            SELECT * FROM roster
            WHERE BILMOS = ?
        ''', (bilmos,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def insert_mos_desc(self, bilmos, description):
        """Insert a new mos description into the mos table."""
        bilmos = str(bilmos)
        self.cursor.execute('''
            INSERT INTO mos (BILMOS, DESCRIPTION)
            VALUES (?, ?)
        ''', (bilmos, description))
        self.conn.commit()

    def update_mos_desc(self, bilmos, description):
        """Update a mos description by BILMOS."""
        bilmos = str(bilmos)
        self.cursor.execute('''
            UPDATE mos
            SET DESCRIPTION = ?
            WHERE BILMOS = ?
        ''', (description, bilmos))
        self.conn.commit()

    def delete_mos_desc(self, bilmos):
        """Delete a mos description by BILMOS."""
        bilmos = str(bilmos)
        self.cursor.execute('''
            DELETE FROM mos
            WHERE BILMOS = ?
        ''', (bilmos,))
        self.conn.commit()

    def get_mos_desc_by_bilmos(self, bilmos):
        """Get MOS description by BILMOS, return as dictionary."""
        bilmos = str(bilmos)
        self.cursor.execute('''
            SELECT * FROM mos
            WHERE BILMOS = ?
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
           Returns as an array of table names.
           {
               "tables": [
                   "table1",
                   "table2"
               ]
           }
        """
        self.cursor.execute('''
            SELECT NAME FROM sqlite_master 
            WHERE TYPE = 'table'
            AND NAME NOT LIKE 'sqlite_%'
        ''')
        tables = [row[0] for row in self.cursor.fetchall()]
        return {"tables": tables}

    def run_query(self, query):
        """
        Runs any query on the database.
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]