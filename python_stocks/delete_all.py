import sqlite3

STOCKS = "stocks.db"

# def delete_all_entries():
#     con = sqlite3.connect(STOCKS)
#     cursor = con.cursor()
#     cursor.execute("DELETE FROM stocks")
#     con.commit()
#     con.close()
#     print("All entries have been deleted.")

# # 全データを削除
# delete_all_entries()

def drop_stocks_table():
    con = sqlite3.connect(STOCKS)
    cursor = con.cursor()
    cursor.execute("DROP TABLE IF EXISTS stocks")
    con.commit()
    con.close()
    print("stocks table has been deleted.")

drop_stocks_table()