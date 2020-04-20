import sqlite3
import csv

DB_NAME = 'nyt_covid19.sqlite'
#create database
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    drop_states_sql = 'DROP TABLE IF EXISTS "States"'
    drop_counties_sql = 'DROP TABLE IF EXISTS "counties"'

    create_states_sql = '''
        CREATE TABLE IF NOT EXISTS "States" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "Date" TEXT NOT NULL,
            "State" TEXT NOT NULL,
            "Fips" INTEGER NOT NULL,
            "Cases" INTEGER NOT NULL,
            "Deaths" INTEGER NOT NULL
        )
    '''
    create_counties_sql = '''
        CREATE TABLE IF NOT EXISTS 'Counties'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Date' INTEGER NOT NULL,
            'County' TEXT NOT NULL,
            'State' TEXT NOT NULL,
            'Fips' INTEGER NOT NULL,
            'Cases' INTEGER NOT NULL,
            'Deaths' INTEGER NOT NULL
        )
    '''

    cur.execute(drop_states_sql)
    cur.execute(drop_counties_sql)
    cur.execute(create_states_sql)
    cur.execute(create_counties_sql)
    conn.commit()
    conn.close()

#read csv, counties and states
def load_counties():
    file_contents_counties = open('us-counties.csv', 'r')
    file_reader_counties = csv.reader(file_contents_counties)
    next(file_reader_counties) # skip header row
    insert_counties_sql = '''
        INSERT INTO Counties
        VALUES (NULL, ?, ?, ?, ?, ?, ?)
    '''
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for c in file_reader_counties:
        cur.execute(insert_counties_sql,
            [
                c[0],
                c[1],
                c[2],
                c[3],
                c[4],
                c[5]
            ]
        )
    conn.commit()
    conn.close()

def load_states():
    file_contents_states = open('us-states.csv', 'r')
    file_reader_states = csv.reader(file_contents_states)
    next(file_reader_states) # skip header row
    # for row in file_reader_states:
    #     print(row)

    insert_states_sql = '''
        INSERT INTO States
        VALUES (NULL, ?, ?, ?, ?, ?)
    '''
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for s in file_reader_states:
        cur.execute(insert_states_sql,
            [
                s[0],
                s[1],
                s[2],
                s[3],
                s[4]
            ]
        )
    conn.commit()
    conn.close()

create_db()
load_counties()
load_states()