import sqlite3 as sql
from datetime import datetime as dt

class Database:
    def __init__(self, dbFile:str):
        self.dbFile = dbFile
        self.initDB()


    def _initConnection(self):
        conn = sql.connect(self.dbFile)
        cursor = conn.cursor()

        return conn, cursor
    

    def _closeConnection(self, conn):
        conn.commit()
        conn.close()


    def initDB(self):
        conn, cursor = self._initConnection()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount1 REAL,
                amount2 REAL,
                share1 REAL,
                share2 REAL,
                date DATE,
                is_shared BOOLEAN,
                proportion1 INTEGER,
                proportion2 INTEGER
            )    
        """)

        self._closeConnection(conn)


    def addRecord(self, category, amount1, amount2, share1, share2, date, is_shared, prop1, prop2):
        conn, cursor = self._initConnection()

        cursor.execute("""
            INSERT INTO expenses (category, amount1, amount2, share1, share2, date, is_shared, proportion1, proportion2)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (category, amount1, amount2, share1, share2, date, is_shared, prop1, prop2))

        self._closeConnection(conn)


    def delRecord(self, recordID):
        conn, cursor = self._initConnection()

        cursor.execute("""
            DELETE FROM expenses WHERE id = ?
        """, (recordID,))

        self._closeConnection(conn)


    def getMonthlyRecords(self, year = str(dt.now().year), month = str(dt.now().month)):
        conn, cursor = self._initConnection()

        year, month = year, month.zfill(2)

        cursor.execute("""
            SELECT id, 
                category,
                amount1, 
                amount2,
                share1,
                share2,
                date
                FROM expenses
            WHERE strftime('%Y-%m', date)=?
        """, (f"{year}-{month}", ))
        
        dbRecords = cursor.fetchall()
        self._closeConnection(conn)

        records = [
            {"id": row[0], 
             "category": row[1], 
             "amount1": row[2], 
             "amount2": row[3], 
             "share1": row[4], 
             "share2": row[5],
             "date": row[6]}
            for row in dbRecords
        ]

        user1 = sum(float(row["share1"] - row["amount1"]) if float(row["share1"] - row["amount1"]) > 0 else 0 for row in records)
        user2 = sum(float(row["share2"] - row["amount2"]) if float(row["share2"] - row["amount2"]) > 0 else 0 for row in records)
        balance = {
            "user1": max(user1 - user2, 0),
            "user2": max(user2 - user1, 0)
        } 

        records.sort(key = lambda x: x["date"], reverse = True)

        return {"records": records, "balance": balance}