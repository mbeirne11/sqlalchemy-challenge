from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from scipy import mean
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# print(f'{engine} this is the engine')
Base = automap_base()
Base.prepare(autoload_with = engine)
Measurement = Base.classes.measurement
Station = Base.classes.station




app = Flask(__name__)

@app.route('/')
def home():
    session = Session(engine)
    last_month = session.query(Measurement).order_by(Measurement.date.desc()).first()
    last_date = last_month.date
    return f'This is the homepage<br>The last date is {last_date}<br>Available routes:<br>/api/v1.0/precipitation<br>/api/v1.0/stations<br>/api/v1.0/tobs<br>/api/v1.0/INSERT START DATE<br>/api/v1.0/INSERT START DATE/INSERT END DATE'

@app.route('/api/v1.0/precipitation')
def percipitation():
    session = Session(engine)
    last_month = session.query(Measurement).order_by(Measurement.date.desc()).first()
    last_date = last_month.date
    last_dates = last_date.split('-')
    last_date_year = int(last_dates[0])
    last_date_month = int(last_dates[1]) 
    last_date_day = int(last_dates[2])
    year_ago = str(dt.date(last_date_year,last_date_month,last_date_day) - dt.timedelta(days = 365))

    data = session.query(Measurement).filter(Measurement.date <= last_date).filter(Measurement.date >= year_ago).all()
    prcps = []
    # transform the data
    for item in data:
        prcps.append({'Date': item.date, 'Percipitaion': item.prcp})
    # return the data
    return jsonify(prcps)

@app.route('/api/v1.0/station')
def station():
    session = Session(engine)
    data = session.query(Measurement.station).distinct(Measurement.station).all()
    stations = []
    # transform the data
    for item in data:
        stations.append(item[0])
    # return the data
    return jsonify(stations)
@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine) 
    last_month = session.query(Measurement).order_by(Measurement.date.desc()).first()
    last_date = last_month.date
    last_dates = last_date.split('-')
    last_date_year = int(last_dates[0])
    last_date_month = int(last_dates[1]) 
    last_date_day = int(last_dates[2])
    year_ago = str(dt.date(last_date_year,last_date_month,last_date_day) - dt.timedelta(days = 365))
   
    data = session.query(Measurement).filter(Measurement.date <= last_date).filter(Measurement.date >= year_ago).all()
    temps = []
    # transform the data
    for item in data:
        temps.append({'Date': item.date, 'Temperatur': item.tobs})
    # return the data
    return jsonify(temps)
@app.route('/api/v1.0/<start>')
def start_stats(start):
    
    session = Session(engine)
    last_month = session.query(Measurement).order_by(Measurement.date.desc()).first()
    last_date = last_month.date

    data = session.query(Measurement).filter(Measurement.date <= last_date).filter(Measurement.date >= start).all()
    temps = []
    if (start <= last_date):
        # transform the data
        for item in data:
            temps.append(item.tobs)
        temp_stats = [{'Start Date': start, 'Min Temperature':min(temps), 'Max Temperature': max(temps), 'Average Temperature': mean(temps)}]
        # return the data
        return jsonify(temp_stats)
    else:
        return "Your start date is after the end date. Please change the date. "
@app.route('/api/v1.0/<start>/<end>')
def start_end_stats(start,end):
    session = Session(engine)
    last_month = session.query(Measurement).order_by(Measurement.date.desc()).first()
    last_date = last_month.date
    data = session.query(Measurement).filter(Measurement.date <= end).filter(Measurement.date >= start).all()
    temps = []
    # transform the data
    if (start < end) and (start <= last_date) and (end <= last_date):
        for item in data:
            temps.append(item.tobs)
        temp_stats = [{'Start Date': start, 'End Date': end, 'Min Temperature':min(temps), 'Max Temperature': max(temps), 'Average Temperature': mean(temps)}]
        # return the data
        return jsonify(temp_stats)
    elif(start > last_date):
        return "Your start date is after the last date. Please change the date. "
    elif(end > last_date):
        return "Your end date is after the last date. Please change the date. "
    else:
        return "Your start date is after the end date. Please change the dates. "

if __name__ == "__main__":
    app.run(debug=True)
