'''
Name:Jinghan Ni
Uniqname: jinghann
Title: Covid-19 Data Insights
'''
from flask import Flask, render_template, request
import requests
import secrets
import sqlite3
import urllib
import requests
import time
import datetime
from datetime import date, timedelta
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots

app = Flask(__name__)

#generate a list of tuples for the top 5 covid-19 news using newsapi, with news titles and matched URL
news_title = []
news_url = []
base_url = 'https://newsapi.org/v2/top-headlines'
params = {
    "q": "Covid-19",
    "language":"en",
    "apiKey": secrets.NEWSAPI_KEY   
}
response = requests.get(base_url, params)
result = response.json()
articles = result["articles"]
for i in articles:
    news_title.append(i['title'])
    if len(news_title) == 5:
        break
for i in articles:
    news_url.append(i['url'])
    if len(news_url) == 5:
        break
news_title_url = list(zip(news_title,news_url))


#populate database in sqlite
DB_NAME = 'nyt_covid19.sqlite'
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

#read file to the database from origin data source, counties and states tables
def load_counties():
    file_contents_counties = urllib.request.urlopen('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
    insert_counties_sql = '''
        INSERT INTO Counties
        VALUES (NULL, ?, ?, ?, ?, ?, ?)
    '''
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    next(file_contents_counties)
    for c in file_contents_counties:
        c = c.decode('utf-8').split(',')
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
    file_contents_states = urllib.request.urlopen('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
    insert_states_sql = '''
        INSERT INTO States
        VALUES (NULL, ?, ?, ?, ?, ?)
    '''
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    next(file_contents_states)
    for s in file_contents_states:
        s = s.decode('utf-8').split(',')
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

#make list to store queried data
states = []
cases = []
deaths = []
dates = []

#Check the latest date in the original data source
def recent_date():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT Date From States")
    for row in cur:
        dates.append(row[0])
    recent_date = max(dates)
    return recent_date

#retrieve data for the first graphic display, overall state covid situation
def query_one():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT State, Cases, Deaths FROM States WHERE date = ? ORDER by Cases DESC",(recent_date(),))
    for row in cur:
        states.append(row[0])
        cases.append(row[1])
        deaths.append(row[2])


#plotly bar graph with latest states data for the index page
@app.route('/')
def plot():
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    fig.add_trace(
    go.Bar(x=states, y=cases, name="Cases"),secondary_y=False,)
    fig.add_trace(go.Bar(x=states, y=deaths, name="Deaths"),secondary_y=True,)
    fig.update_xaxes(title_text="States", tickangle=45)
    fig.update_yaxes(title_text="<b>primary</b> Cases", secondary_y=False,range = [0,max(cases)+10000]) #how to hid the secondary Y axis
    fig.update_yaxes(title_text="<b>secondary</b> Deaths", secondary_y=True,range = [0,max(cases)+10000])
    div = fig.to_html(full_html=False)
    #return values
    return render_template("index.html", plot_div=div, recent_date = recent_date(),news_title_url = news_title_url)

#plot county data for the user select states
@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    counties = []
    cases_counties = []
    deaths_counties = []
    mapped = zip(counties, cases_counties, deaths_counties) 
    state_input = request.form["state_input"]
    #query for state specific data
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    results = cur.execute("SELECT County, Cases, Deaths FROM Counties WHERE date = ? and State = ? ORDER by Cases DESC",(recent_date(),state_input))
    for row in results:
        counties.append(row[0])
        cases_counties.append(row[1])
        deaths_counties.append(row[2])
    #ploting, show cases and deaths on the same graph
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=counties, y=cases_counties, name="Cases"),secondary_y=False,)
    fig.add_trace(go.Bar(x=counties, y=deaths_counties, name="Deaths"),secondary_y=True,)
    fig.update_xaxes(title_text="Counties", tickangle=45)
    fig.update_yaxes(title_text="<b>primary</b> Cases", secondary_y=False,range = [0,max(cases_counties)+1000]) #how to hid the secondary Y axis
    fig.update_yaxes(title_text="<b>secondary</b> Deaths", secondary_y=True,range = [0,max(cases_counties)+1000])
    div = fig.to_html(full_html=False)
    #return values
    return render_template("test.html", plot_div_two=div,state_input = state_input,mapped = mapped,recent_date = recent_date())

if __name__ == '__main__':
    create_db()
    load_counties()
    load_states()
    recent_date()
    query_one()
    app.run(debug=True)