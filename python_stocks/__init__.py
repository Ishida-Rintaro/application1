from flask import Flask
app = Flask(__name__)
import python_stocks.main
from python_stocks import db
db.create_stocks_table()
