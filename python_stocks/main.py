from python_stocks import app
from flask import render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
STOCKS="stocks.db"

def create_stocks_table():
    con = sqlite3.connect(STOCKS)
    cursor = con.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            name TEXT,
            degree TEXT,
            number TEXT PRIMARY KEY,
            quantity INTEGER,
            arrival_date TEXT,
            memo TEXT
        )
    ''')
    con.commit()
    con.close()
create_stocks_table()
# stocks=[]

@app.route('/')
def index():
     con=sqlite3.connect(STOCKS)
     db_stocks=con.execute('SELECT*FROM stocks').fetchall()
     con.close()
     stocks= []
     for row in db_stocks:
         stocks.append ({'name':row[0], 'degree':row[1], 'number':row[2],'quantity':row[3],'arrival_date':row[4],'memo':row[5]})
     return render_template('index.html'
                            , stocks=stocks)

@app.route('/register')
def register():
    today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    return render_template('register.html', today=today)

@app.route('/add')
def add():
     con=sqlite3.connect(STOCKS)
     db_stocks=con.execute('SELECT*FROM stocks').fetchall()
     con.close()
     stocks= []
     for row in db_stocks:
         stocks.append ({'name':row[0], 'degree':row[1], 'number':row[2],'quantity':row[3],'arrival_date':row[4],'memo':row[5]})
     return render_template('add.html', stocks=stocks)

@app.route('/delete')
def delete():
    con=sqlite3.connect(STOCKS)
    db_stocks=con.execute('SELECT*FROM stocks').fetchall()
    con.close()
    stocks= []
    for row in db_stocks:
          stocks.append({'name':row[0], 'degree':row[1], 'number':row[2],'quantity':row[3],'arrival_date':row[4],'memo':row[5]})
    return render_template('delete.html', stocks=stocks)

@app.route('/edit')
def edit():
    con=sqlite3.connect(STOCKS)
    db_stocks=con.execute('SELECT*FROM stocks').fetchall()
    con.close()
    stocks= []
    for row in db_stocks:
          stocks.append({'name':row[0], 'degree':row[1], 'number':row[2],'quantity':row[3],'arrival_date':row[4],'memo':row[5]})
    return render_template('edit.html', stocks=stocks)


@app.route('/entry', methods=['POST'])
def entry():
    name = request.form['name']
    degree = request.form['degree']
    number = request.form['number']
    quantity = int(request.form['quantity'])
    arrival_date = request.form['arrival_date']
    memo = request.form['memo']

    con = sqlite3.connect(STOCKS)
    cursor = con.cursor()
    today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    # `number`が既存データにあるか確認
    cursor.execute("SELECT * FROM stocks WHERE number = ? AND name = ? AND degree = ?", (number, name, degree))
    existing_stock = cursor.fetchone()

    if existing_stock:
        # データが存在する場合は数量を更新
        cursor.execute("UPDATE stocks SET quantity = quantity + ?, arrival_date = ? WHERE number = ?", (quantity, today, number))
        con.commit()
        return redirect(url_for('register'))
    else:
        cursor.execute("SELECT * FROM stocks WHERE number = ? ", (number,))
        existing_stock2 = cursor.fetchone()
        if existing_stock2:
          return redirect(url_for('escape'))
        else:
        # データが存在しない場合は新規登録
          cursor.execute("INSERT INTO stocks (name, degree, number, quantity, arrival_date, memo) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, degree, number, quantity, arrival_date, memo))

    con.commit()
    cursor.close()
    con.close()
    return redirect(url_for('register'))

@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    number = request.form['number']
    quantity = int(request.form['quantity'])  # 削除個数を取得

    con = sqlite3.connect(STOCKS)
    cursor = con.cursor()

    # 現在の数量を取得
    cursor.execute("SELECT quantity FROM stocks WHERE number = ?", (number,))
    current_stock = cursor.fetchone()

    if current_stock:
        current_quantity = current_stock[0]
        if quantity == current_quantity:
            # 削除個数が現在の数量以上の場合、レコードを削除
            cursor.execute("DELETE FROM stocks WHERE number = ?", (number,))
        elif quantity < current_quantity:
            today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            # 削除個数が現在の数量未満の場合、数量を減らす
            cursor.execute("UPDATE stocks SET quantity = quantity - ?, arrival_date =?  WHERE number = ?", (quantity, today, number))
        else: 
            # 削除個数が現在の数量より多い場合、エラーメッセージを表示
            return "削除個数が現在の数量を超えています。在庫一覧を確認してください", 400
        
    con.commit()
    cursor.close()
    con.close()
    return redirect(url_for('delete'))

@app.route('/sort_by_arrival_date', methods=['POST','GET'])
def sort_by_arrival_date():
    con=sqlite3.connect(STOCKS)
    db_stocks=con.execute('SELECT*FROM stocks ORDER BY arrival_date DESC').fetchall()
    con.close()
    stocks= []
    for row in db_stocks:
       stocks.append({'name':row[0], 'degree':row[1], 'number':row[2],'quantity':row[3],'arrival_date':row[4],'memo':row[5]})
    return render_template('index.html', stocks=stocks)

@app.route('/sort_by_quantity', methods=['POST','GET'])
def sort_by_quantity():
    con=sqlite3.connect(STOCKS)
    db_stocks=con.execute('SELECT*FROM stocks ORDER BY quantity DESC').fetchall()
    con.close()
    stocks= []
    for row in db_stocks:
         stocks.append({'name':row[0], 'degree':row[1], 'number':row[2],'quantity':row[3],'arrival_date':row[4],'memo':row[5]})
    return render_template('index.html', stocks=stocks)

@app.route('/search_delete', methods=['POST','GET'])
def search_delete():
    if request.method == 'POST':
        # フォームから送信された製品番号を取得
        request_number = request.form.get('number')
    else:
        # GETリクエストの場合、クエリパラメータから取得
        request_number = request.args.get('number')

    if not request_number:
        return "製品番号が指定されていません", 400

    con = sqlite3.connect(STOCKS)
    cursor = con.cursor()

    # データベースから該当する製品を検索
    cursor.execute("SELECT * FROM stocks WHERE number = ?", (request_number,))
    stock = cursor.fetchone()
    con.close()

    if stock:
        # 製品が見つかった場合、テンプレートにデータを渡す
        stock_data = {'name': stock[0], 'degree': stock[1], 'number': stock[2],
                      'quantity': stock[3], 'arrival_date': stock[4], 'memo': stock[5]}
        return render_template('delete.html', stocks=[stock_data])
    else:
        # 製品が見つからなかった場合
        return render_template('escape2.html')

@app.route('/search_add', methods=['POST','GET'])
def search_add():
    if request.method == 'POST':
        # フォームから送信された製品番号を取得
        request_number = request.form.get('number')
    else:
        # GETリクエストの場合、クエリパラメータから取得
        request_number = request.args.get('number')

    if not request_number:
        return "製品番号が指定されていません", 400

    con = sqlite3.connect(STOCKS)
    cursor = con.cursor()

    # データベースから該当する製品を検索
    cursor.execute("SELECT * FROM stocks WHERE number = ?", (request_number,))
    stock = cursor.fetchone()
    con.close()

    if stock:
        # 製品が見つかった場合、テンプレートにデータを渡す
        stock_data = {'name': stock[0], 'degree': stock[1], 'number': stock[2],
                      'quantity': stock[3], 'arrival_date': stock[4], 'memo': stock[5]}
        return render_template('add.html', stocks=[stock_data])
    else:
        # 製品が見つからなかった場合
        return "該当する製品が見つかりませんでした", 404

@app.route('/sort_by_arrival_date2', methods=['POST','GET'])
def sort_by_arrival_date2():
    con=sqlite3.connect(STOCKS)
    db_stocks=con.execute('SELECT*FROM stocks ORDER BY arrival_date DESC').fetchall()
    con.close()
    stocks= []
    for row in db_stocks:
         stocks.append({'name':row[0], 'degree':row[1], 'number':row[2],'quantity':row[3],'arrival_date':row[4],'memo':row[5]})
    return render_template('delete.html', stocks=stocks)

@app.route('/sort_by_quantity2', methods=['POST','GET'])
def sort_by_quantity2():
    con=sqlite3.connect(STOCKS)
    db_stocks=con.execute('SELECT*FROM stocks ORDER BY quantity DESC').fetchall()
    con.close()
    stocks= []
    for row in db_stocks:
          stocks.append({'name':row[0], 'degree':row[1], 'number':row[2],'quantity':row[3],'arrival_date':row[4],'memo':row[5]})
    return render_template('delete.html', stocks=stocks)

@app.route('/escape')
def escape():
    return render_template('escape.html')

@app.route('/add_entry', methods=['POST'])
def add_entry():
    number = request.form['number']
    quantity = int(request.form['quantity'])  # 削除個数を取得
    today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    con = sqlite3.connect(STOCKS)
    cursor = con.cursor()

    # 現在の数量を取得
    cursor.execute("SELECT quantity FROM stocks WHERE number = ?", (number,))
    cursor.execute("UPDATE stocks SET quantity = quantity + ?, arrival_date = ? WHERE number = ?", (quantity, today, number))
    con.commit()
    cursor.close()
    con.close()
    return redirect(url_for('add'))

@app.route('/edit_form', methods=['POST', 'GET'])
def edit_form():
    if request.method == 'POST':
        number = request.form.get('number')  # フォームから製品番号を取得
    else:
        number = request.args.get('number')  # GETリクエストの場合
    today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    con = sqlite3.connect(STOCKS)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM stocks WHERE number = ?", (number,))
    stock = cursor.fetchone()
    con.close()
    stock_data = {'name': stock[0], 'degree': stock[1], 'number': stock[2],
                      'quantity': stock[3], 'arrival_date': stock[4], 'memo': stock[5]}
    return render_template('edit.html', today = today, stocks=[stock_data], stock_number = stock[2])  # 単一のデータを渡す
  
@app.route('/edit_entry', methods=['POST'])
def edit_entry():
    name = request.form['name']
    degree = request.form['degree']
    number = request.form['number']
    quantity = int(request.form['quantity'])
    arrival_date = request.form['arrival_date']
    memo = request.form['memo']
    today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    con = sqlite3.connect(STOCKS)
    cursor = con.cursor()

    # データを更新
    cursor.execute("UPDATE stocks SET name = ?, degree = ?, quantity = ?, arrival_date = ?, memo = ? WHERE number = ?",
                   (name, degree, quantity, arrival_date, memo, number))

    con.commit()
    cursor.close()
    con.close()
    return redirect(url_for('index'))