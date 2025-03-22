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
                is_shared,
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
             "is_shared": row[6],
             "date": row[7]}
            for row in dbRecords
        ]

        records.sort(key = lambda x: x["date"], reverse = True)

        user1_balance = sum(float(row["share1"] - row["amount1"]) if float(row["share1"] - row["amount1"]) > 0 else 0 for row in records)
        user2_balance = sum(float(row["share2"] - row["amount2"]) if float(row["share2"] - row["amount2"]) > 0 else 0 for row in records)
        user1_balance -= user2_balance
        user2_balance = -user1_balance
        balance = {
            "user1": max(round(user1_balance, 2), 0),
            "user2": max(round(user2_balance, 2), 0)
        } 

        summary = {}
        user1_summary = round(sum(float(row["amount1"]) for row in records) + user1_balance, 2)
        user2_summary = round(sum(float(row["amount2"]) for row in records) + user2_balance, 2)

        if user1_summary:
            summary["user1"] = {
                "overall": user1_summary,
                "food": round(sum(float(row["share1"]) if row["category"] == "Food" else 0.0 for row in records), 2),
                "clothes": round(sum(float(row["share1"]) if row["category"] == "Clothes" else 0.0 for row in records), 2),
                "cosmetics": round(sum(float(row["share1"]) if row["category"] == "Cosmetics" else 0.0 for row in records), 2),
                "fun": round(sum(float(row["share1"]) if row["category"] == "Fun" else 0.0 for row in records), 2),
                "travel": round(sum(float(row["share1"]) if row["category"] == "Travel" else 0.0 for row in records), 2),
                "others": round(sum(float(row["share1"]) if row["category"] == "Others" else 0.0 for row in records), 2)
            }

        if user2_summary:
            summary["user2"] = {
                "overall": user2_summary,
                "food": round(sum(float(row["share2"]) if row["category"] == "Food" else 0.0 for row in records), 2),
                "clothes": round(sum(float(row["share2"]) if row["category"] == "Clothes" else 0.0 for row in records), 2),
                "cosmetics": round(sum(float(row["share2"]) if row["category"] == "Cosmetics" else 0.0 for row in records), 2),
                "fun": round(sum(float(row["share2"]) if row["category"] == "Fun" else 0.0 for row in records), 2),
                "travel": round(sum(float(row["share2"]) if row["category"] == "Travel" else 0.0 for row in records), 2),
                "others": round(sum(float(row["share2"]) if row["category"] == "Others" else 0.0 for row in records), 2)
            }

        return {"records": records, "balance": balance, "summary": summary}