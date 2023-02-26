import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
from dateutil.relativedelta import relativedelta


# Database Setup
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Reflect an existing database into a new model.
Base = automap_base()

# Reflect the tables.
Base.prepare(engine, reflect=True)

# Save reference to the tables.
Measurement = Base.classes.measurement
Station = Base.classes.station
print(Base.classes.keys())

# Flask Setup

app = Flask(__name__)

# Flask Routes

# Home Page
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Welcome to the SQL-Alchemy!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date:yyyy-mm-dd]/[end_date:yyyy-mm-dd]<br/>"
    )

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session from Python to the DB
    session = Session(engine)

    """Return a list of all Precipitation Data"""
    # Query all precipitation
    last_year_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > '2016-08-23').\
        order_by(Measurement.date).all()

    session.close()
    
    # Create dictionary for precipitation last_year_data
    all_prcp = []
    for date,prcp  in last_year_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

#Station Routes
@app.route("/api/v1.0/stations")
def stations():
    # Create session from Python to the DB
    session = Session(engine)

    """Return a list of all Stations"""
    # Query all station's id and name 
    station_data = session.query(Station.station, Station.name).\
                 order_by(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station_data))

    return jsonify(all_stations)

# TOBSs Route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create session from Python to the DB
    session = Session(engine)

    """Return a list of all TOBs"""
    # Query all tobs
    tobs_data = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station=='USC00519281').\
                order_by(Measurement.date).all()

    session.close()

   
    # Create tobs_data dictionary
    all_tobs = []
    for date, tobs, prcp in tobs_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_dict["prcp"] = prcp

        all_tobs.append(tobs_dict) 

    return jsonify(all_tobs)

# Start Date Variable Route    
@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
    # Create session from Python to the DB
    session = Session(engine)

    """Return a list of min, avg and max tobs for a start date"""
    # Query all tobs
    start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

    session.close()

    # Create a dictionary for start_date_tobs
    start_date_tobs = []
    for min, avg, max in start:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs_dict) 
    return jsonify(start_date_tobs)

# Start and End Date Variable Route
@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    # Create session from Python to the DB
    session = Session(engine)

    """Return a list of min, avg and max tobs for start and end dates"""
    # Query all tobs for start and end date data
    start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()
  
    # Create a dictionary for start_end data
    start_end_tobs = []
    for min, avg, max in start_end:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    
    return jsonify(start_end_tobs)

if __name__ == "__main__":
    app.run(debug=True)