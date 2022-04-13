import sqlite3


def create_table():
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
       wid int PRIMARY KEY,
       website TEXT,
       progress TEXT,
       progress2018 TEXT,
       progress2019 TEXT,
       progress2020 TEXT,
       progress2021 TEXT,
       comment TEXT);
    """)
    conn.commit()


def create_companies_db():
    conn = sqlite3.connect('companies.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS companies(
           bin TEXT,
           fio TEXT,
           gov_reg TEXT,
           address TEXT,
           date_definition TEXT,
           date_nomination TEXT,
           date_temp_manager TEXT,
           fio_temp_manager TEXT,
           date_accept_from TEXT,
           date_accept_till TEXT,
           address_reception TEXT,
           contact_number int,
           date_registration TEXT);
        """)
    conn.commit()


def delete_all_info_companies():
    conn = sqlite3.connect('companies.db')
    cur = conn.cursor()
    cur.execute("Delete from companies")
    conn.commit()
