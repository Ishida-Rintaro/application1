import sqlite3
STOCKS="stocks.db"
def create_stocks_table():
    con=sqlite3.connect(STOCKS)
    con.execute("CREATE TABLE IF NOT EXISTS stocks (name, degree, number, quantity, arrival_date, memo)")
    con.close()
    