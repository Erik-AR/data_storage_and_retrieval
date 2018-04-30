from  flask import Flask,jsonify
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the invoices and invoice_items tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii weather analysis API!:<br\>"
        f"Availeble Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"

        f"/api/v1.0/stations"
        f"- List of stations<br/>"

        f"/api/v1.0/tobs"
        f"- List of Temperature Observations<br/>"

        f"/api/v1.0/<\start><br/>"
        f"/api/v1.0/<\start>/<\end>"
        f"- Start and End Dates<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation"""
    # Query all precipitation from measurement table
    begin_date = '2016-08-22'
    end_date = '2017-08-23'
    month_range = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >=begin_date).filter(Measurement.date <= end_date).all()

    data_dict = {}
    for row in month_range:
        data_dict[row[0]]=row[1]

    return jsonify(data_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset."""
    # Query all stations from station table
    stations_list = session.query(Station.station).all()
    return jsonify(list(stations_list))


@app.route('/api/v1.0/tobs')
def tobs():
    """Return a json list of Temperature Observations (tobs) for the previous year"""
    begin_date = '2016-08-22'
    end_date = '2017-08-23'
    tobs_list = session.query(Measurement.tobs).filter(Measurement.date >= begin_date).filter(Measurement.date <= end_date).all()
    return jsonify(list(tobs_list))

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def calc_temps(start = dt.datetime(2016,8, 23),end = False):
    """Return temperatures for user input dates. If no end date, use all available"""
    if end != False:
        results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>= start).filter(Measurement.date <= end).all()
    else:
        results =session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>= start).all()
    temp_dict = {'tmin':results[0][0],'tmax':results[0][1],'tavg':results[0][2]}
    return jsonify(temp_dict)





if __name__ == '__main__':
    app.run(debug=True)