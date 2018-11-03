from flask import Flask,jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func
import pandas as pd
from datetime import datetime
import datetime as dt

# Database Setup

engine=create_engine("sqlite:///Resources/hawaii.sqlite")
Base=automap_base()
Base.prepare(engine,reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Flask Setup

app=Flask(__name__)

#Flask Routes

@app.route("/")
def welcome():
  # """List all available routes"""
   return(
       f"Available Routes:<br/>"
       f"/api/v1.0/precipitation</br/>"
       f"/api/v1.0/stations<br/>"
       f"/api/v1.0/tobs<br/>"
       f"/api/v1.0/<start><br/>"
       f"/api/v1.0/<start>/<end>"
   )
@app.route("/api/v1.0/precipitation")
def precipitation():
       #"""Return the JSON representation of Precipitation"""
       ##most_recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago=dt.date(2017, 10, 28)-dt.timedelta(days=365)

        # Perform a query to retrieve the data and precipitation scores # Sort the dataframe by date

    data_precipitation=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=year_ago).order_by(Measurement.date).all()
    precipitation_result=list(np.ravel(data_precipitation))
    return jsonify(precipitation_result)

@app.route("/api/v1.0/stations")
def stations():
    #Return a JSON list of stations from the dataset.
    station_list=session.query(Station.station,Station.name).all()
    Station_list=list(np.ravel(station_list))
    return jsonify(Station_list)

@app.route("/api/v1.0/tobs")
def temperature():
    #Return a JSON list of Temperature Observations (tobs) for the previous year.
   year_ago=dt.date(2017, 8, 23)-dt.timedelta(days=365)
   temperatures_precipitation=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>=year_ago).order_by(Measurement.date).all()
   temperatures=list(np.ravel(temperatures_precipitation))
   return jsonify(temperatures)
@app.route("/api/v1.0/")
def temperature_start(start,methods=['GET']):
    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    #When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    result= session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) == start).all()
    temperature_range= list(np.ravel(result))
    return jsonify(temperature_range)
@app.route("/api/v1.0/start/end")
def temperature_stats(start,end):
    #When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    result=session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date)>=start).filter(func.strftime("%Y-%m-%d", Measurement.date)<= end).all()
    temp_range= list(np.ravel(result))
    return jsonify(temp_range)
if __name__ == '__main__':
    app.run(debug=True)