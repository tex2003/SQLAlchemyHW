import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br> "  
        f"/api/v1.0/start/<start><br>"
        f"/api/v1.0/start/<start>/end/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    latest = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()
    all_prcp = []
    for station in results:
        precipitation_dict = {}
        precipitation_dict["date"] = Measurement.date
        precipitation_dict["precipitation"] = Measurement.prcp
        all_prcp.append(precipitation_dict)
    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()
    location = list(np.ravel(results))
    return jsonify(location)

@app.route("/api/v1.0/tobs")
def tobs():
    latest = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)    
    results = session.query(Measurement.tobs).filter(Measurement.date >= query_date).all()
    tobs = list(np.ravel(results))
    return jsonify(tobs)

@app.route("/api/v1.0/start/<start>")
def describe(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    description = list(np.ravel(results))
    return jsonify(description)

@app.route("/api/v1.0/start/<start>/end/<end>")
def describe2(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    description2 = list(np.ravel(results))
    return jsonify(description2)

if __name__ == '__main__':
    app.run(debug=True)
