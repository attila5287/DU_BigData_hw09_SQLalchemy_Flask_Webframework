# dependencies
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import sqlalchemy
from flask import Flask, jsonify
import datetime as dt
# Write a function called `calc_temps` that will accept start date and end date in the format '%Y-%m-%d' and return the minimum, average, and maximum temperatures for that range of dates


def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.

    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d

    Returns:
        TMIN, TAVE, and TMAX
    """

    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(
            Measurement.date <= end_date).all()
# Create a query that will calculate the daily normals=avg(min,max,mean)


def daily_normals(date):
    """Daily Normals.
    Args:
        date (str): A date string in the format '%m-%d'
    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax
    """
# --------------------
    sel = [func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
# flask routes and text messages
app = Flask(__name__)
# decorator and text


@app.route("/")
def welcome():
    return (
        "Welcome to Hawaii Climate App API!<br><br>"
        " Available Routes:<br><br>"
        "/api/v1.0/precipitation<br><br>"
        "/api/v1.0/stations<br><br>"
        "/api/v1.0/tobs<br><br>"
        "/api/v1.0/StartDate As %m-%d<br><br>"
        "/api/v1.0/StartDate As %Y-%m-%d/EndDate as %Y-%m-%d"

    )
# --------
# Precipitation Route
#   * Query for the dates and temperature observations from the last year.
#   * Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
#   * Return the JSON representation of your dictionary.


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of Temperature observations including date and tobs"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date.between('2016-08-23', '2017-08-23')).\
        order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    tobs = []
    for tob in results:
        tobs_dict = {}
        tobs_dict["Date"] = tob.date
        tobs_dict["TOBS"] = tob.tobs
        tobs.append(tobs_dict)

    return jsonify(tobs)
# ------------
# Station Routes-JSON formatted lists


@app.route("/api/v1.0/stations")
def stations():
    """Return the Stations as json"""

    results = session.query(Measurement.station).all()

    stations = []
    for station in results:
        stat_dict = {}
        stat_dict["Stations"] = station.station
        stations.append(stat_dict)
    return jsonify(stations)
# Tobs Routes*JSON format tobs: temperature observed


@app.route("/api/v1.0/tobs")
def tobs():
    """Return the TOBS as json"""

    results = session.query(Measurement.tobs).\
        filter(Measurement.date.between('2016-08-23', '2017-08-23')).\
        order_by(Measurement.date).all()
    # dict from the row data created then appended to a list of all_passengers
    tobs = []
    for tob in results:
        tobs_dict = {}
        tobs_dict["TOBS"] = tob.tobs
        tobs.append(tobs_dict)

    return jsonify(tobs)
# Date Routes
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.


@app.route("/api/v1.0/<start>")
def temp(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range"""

    results = daily_normals(start)

    temps = []
    for temp in results:
        temp_dict = {}
        temp_dict["TMIN"] = temp[0]
        temp_dict["TAVG"] = temp[1]
        temp_dict["TMAX"] = temp[2]
        temps.append(temp_dict)

    return jsonify(temps)


@app.route("/api/v1.0/<start>/<end>")
def tempend(start, end):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range"""

    results = calc_temps(start, end)

    temps = []
    for temp in results:
        temp_dict = {}
        temp_dict["TMIN"] = temp[0]
        temp_dict["TAVG"] = temp[1]
        temp_dict["TMAX"] = temp[2]
        temps.append(temp_dict)

    return jsonify(temps)


if __name__ == "__main__":
    app.run(debug=True)
