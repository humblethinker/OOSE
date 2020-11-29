import sqlite3
import json
with open('C:/Users/humbl/Downloads/OOSE/config.json') as data_file:
    config = json.load(data_file)

conn=sqlite3.connect(config['database'], check_same_thread=False)
conn.execute('pragma foreign_keys=ON')



def dict_factory(cursor, row):
    """This is an function use to format the json when retrieve from the mysql database"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn.row_factory = dict_factory

conn.execute('''CREATE TABLE if not exists patient
(pat_id INTEGER PRIMARY KEY AUTOINCREMENT,
pat_first_name TEXT NOT NULL,
pat_last_name TEXT NOT NULL,
age INTEGER NOT NULL,
sex TEXT NOT NULL,
bed_id INTEGER NOT NULL,
charges INTEGER NOT NULL DEFAULT 0,
pat_ph_no INTEGER NOT NULL,
tests TEXT NOT NULL DEFAULT "No test record",
diagnosis TEXT NOT NULL DEFAULT "No diagnosis record",
pat_date DATE DEFAULT (datetime('now','localtime')),
discharge_date DATE DEFAULT (datetime('now','localtime')),
pat_address TEXT NOT NULL);''')

conn.execute('''CREATE TABLE if not exists user
(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_first_name TEXT NOT NULL,
user_last_name TEXT NOT NULL,
user_ph_no TEXT NOT NULL,
age INTEGER NOT NULL,
sex TEXT NOT NULL,
password TEXT NOT NULL DEFAULT "1234567",
designation TEXT NOT NULL,
user_date DATE DEFAULT (datetime('now','localtime')),
user_address TEXT NOT NULL);''')

conn.execute('''CREATE TABLE if not exists appointment
(app_id INTEGER PRIMARY KEY AUTOINCREMENT,
pat_id INTEGER NOT NULL,
user_id INTEGER NOT NULL,
appointment_date DATE NOT NULL,
FOREIGN KEY(pat_id) REFERENCES patient(pat_id),
FOREIGN KEY(user_id) REFERENCES user(user_id));''')

conn.execute('''CREATE TABLE if not exists bed
(bed_id INTEGER PRIMARY KEY AUTOINCREMENT,
pat_id INTEGER);''')

conn.execute('''CREATE TABLE if not exists medicine
(med_id INTEGER PRIMARY KEY AUTOINCREMENT,
med_name TEXT NOT NULL UNIQUE,
uses TEXT NOT NULL,
quant INTEGER NOT NULL);''')

conn.execute('''CREATE TABLE if not exists payment
(payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
pat_id TEXT NOT NULL UNIQUE,
amount INTEGER NOT NULL,
FOREIGN KEY(pat_id) REFERENCES patient(pat_id));''')