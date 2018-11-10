from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import sqlalchemy
from flask import Flask, jsonify
import datetime as dt
import numpy as np


# - SQLalchemy to reflect database from SQLite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


# Flask setup and home page
app = Flask(__name__)

# route_0: index or home page


@app.route('/')
def index():
    pass
    return(
        "<dd><dl><br><h2>Available Routes:<h2></dl></dd>"
        "<h4>/api/v1.0/stations<br/></h4>"
        "<dd> *  lists the stations and their observation codes</dd> "
        "<h4><br>/api/v1.0/tobs</h4>"
        "<dd> *  finds the most recent date on the dataset and brings the last twelve months Temperature observation data with units in Fahrenheit </dd> "
        "<h4>/api/v1.0/precipitation<br/></h4>"
        "<dd> *  finds the most recent date on the dataset and brings the last twelve months Precipitation observation data with units in inches</dd>"
        "<h4>/api/v1.0/<start></h4>"
        "<dd> *  start date- via API request- required at the end of the url</dd>"
        "<dd> *  calculates Minimum, Average and Maximum Temperature values </dd> "
        "<dd> *  displays a json format list with  above temp values</dd>"
        "<h4>/api/v1.0/<start>/<end></h4>"
        "<dd> *  start and end dates separated by a slash / required at the end of the url via api request</dd><br/>"
    )


#  first route for stations, briefly returns json list of station names and codes


@app.route("/api/v1.0/stations")
def stations():
    pass
    station_list = session.query(Station.station, Station.name).all()
    Station_list_flat = list(np.ravel(station_list))

    return jsonify(Station_list_flat)


# second route for Temperature data:  returns json format in Fahrenheit as units
# file also saved as  '/tobs_web_pag.json' within the same folder
@app.route("/api/v1.0/tobs")
def last12mo_tobs():
    pass
    query_for_ayearago = session.query(Measurement.date).\
        order_by(Measurement.date).all()
    #  - -
    latest_year = int(query_for_ayearago[-1][0][:4])
    latest_mm = int(query_for_ayearago[-1][0][5:7])
    latest_dd = int(query_for_ayearago[-1][0][8:10])
    # - -
    ayearago_dt = dt.date(latest_year, latest_mm, latest_dd) - \
        dt.timedelta(days=365)
    # - -
    query_for_tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date.
               between(query_for_ayearago[0][0], query_for_ayearago[-1][0])).\
        order_by(Measurement.date).all()

    tobs_list = []

    for observation in query_for_tobs:
        tobs_dict = {}
        tobs_dict["Date"] = observation.date
        tobs_dict["Temp"] = observation.tobs
        tobs_list.append(tobs_dict)
        # print(observation)
        # ---
    return jsonify(list(np.ravel(tobs_list)))
#

# third route for Precipitation data:  returns json format in inches as unit
# file also saved as  '/precipitation_web_page.json' within the same folder


@app.route('/api/v1.0/precipitation')
def last12mo_prcp():
    pass
    query_for_ayearago = session.query(Measurement.date).\
        order_by(Measurement.date).all()
    #  - -
    latest_year = int(query_for_ayearago[-1][0][:4])
    latest_mm = int(query_for_ayearago[-1][0][5:7])
    latest_dd = int(query_for_ayearago[-1][0][8:10])
    # - -
    ayearago_dt = dt.date(latest_year, latest_mm, latest_dd) - \
        dt.timedelta(days=365)
    # - -
    query_for_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date.
               between(query_for_ayearago[0][0], query_for_ayearago[-1][0])).\
        order_by(Measurement.date).all()

    prcp_list = []

    for observation in query_for_prcp:
        prcp_dict = {}
        prcp_dict["Date"] = observation.date
        prcp_dict["Precipitation"] = observation.prcp
        prcp_list.append(prcp_dict)
        # print(observation)
        # ---``

    return jsonify(list(np.ravel(prcp_list)))

# fourth route: * requires API request for <start> date
#  function tested in file 'testfunc_startdate_temp_min_avg_max.py' same directory


@app.route('/api/v1.0/<start>')
def temps_MinAvgMax_startdate(start):
    pass
    start_date = start
    # find the most recent date on the dataset
    query_for_mostrecent = session.query(Measurement.date).\
        order_by(Measurement.date).all()
    # etract year, month and day of the date before dt method
    mostrecent_year = int(query_for_mostrecent[-1][0][:4])
    mostrecent_mm = int(query_for_mostrecent[-1][0][5:7])
    mostrecent_dd = int(query_for_mostrecent[-1][0][8:10])

# - extract digits for year, month and day; then call module dt for date
    mostrecent_date = dt.date(mostrecent_year, mostrecent_mm, mostrecent_dd)

# - - query from SQLite
    min_temp_query = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= mostrecent_date).\
        order_by(Measurement.date).all()

    avg_temp_query = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= mostrecent_date).\
        order_by(Measurement.date).all()

    max_temp_query = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= mostrecent_date).\
        order_by(Measurement.date).all()

    # create a list to store dictioneries  before jsonify output
    # note the aim is to create a list of dictionaries for json
    startdate_list_dicts = []

    # define  dictionaries to be stored in a list as variables
    min_temp_dict = {}

    # key for dict where temp value will be paired
    min_temp_key = 'Minimum Temperature'

    # result object consisting of tuples thus temp should be extracted
    # note index[0]~[0] here should not be confused with manual entry
    min_temp_value = np.ravel(min_temp_query[0])[0]

    # key : value for the first dict
    min_temp_dict = {min_temp_key: min_temp_value}

    # append first dict to list of dicts
    startdate_list_dicts.append(min_temp_dict)

    # same procedure above
    avg_temp_dict = {}
    avg_temp_value = np.ravel(avg_temp_query[0])[0]
    avg_temp_key = 'Average Temperature'
    avg_temp_dict[avg_temp_key] = avg_temp_value

    # append second dict to list of dicts
    startdate_list_dicts.append(avg_temp_dict)

    # same procedure with first dict explained in detail above
    max_temp_dict = {}
    max_temp_value = np.ravel(max_temp_query[0])[0]
    max_temp_key = 'Maximum Temperature'
    max_temp_dict[max_temp_key] = max_temp_value

    # append third dict to list of dicts
    startdate_list_dicts.append(max_temp_dict)
    return jsonify(list(np.ravel(startdate_list_dicts)))

# fifth/last route: * requires API request for <start> and <end> dates
#  function tested in file 'testfunc_startenddates_temp_min_avg_max.py' same directory


@app.route('/api/v1.0/<start>/<end>')
def temps_MinAvgMax_startenddates(start, end):
    pass
    start_date = start
    end_date = end

# - - query from SQLite
    min_temp_query = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        order_by(Measurement.date).all()

    avg_temp_query = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        order_by(Measurement.date).all()

    max_temp_query = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        order_by(Measurement.date).all()

    # create a list to store dictioneries  before jsonify output
    # note the aim is to create a list of dictionaries for json
    endstartdate_list_dicts = []

    # define  dictionaries to be stored in a list as variables
    min_temp_dict = {}

    # key for dict where temp value will be paired
    min_temp_key = 'Minimum Temperature'

    # result object consisting of tuples thus temp should be extracted
    # note index[0]~[0] here should not be confused with manual entry
    min_temp_value = np.ravel(min_temp_query[0])[0]

    # key : value for the first dict
    min_temp_dict = {min_temp_key: min_temp_value}

    # append first dict to list of dicts
    endstartdate_list_dicts.append(min_temp_dict)

    # same procedure above
    avg_temp_dict = {}
    avg_temp_value = np.ravel(avg_temp_query[0])[0]
    avg_temp_key = 'Average Temperature'
    avg_temp_dict[avg_temp_key] = avg_temp_value

    # append second dict to list of dicts
    endstartdate_list_dicts.append(avg_temp_dict)

    # same procedure with first dict explained in detail above
    max_temp_dict = {}
    max_temp_value = np.ravel(max_temp_query[0])[0]
    max_temp_key = 'Maximum Temperature'
    max_temp_dict[max_temp_key] = max_temp_value

    # append third dict to list of dicts
    endstartdate_list_dicts.append(max_temp_dict)

    return jsonify(list(np.ravel(endstartdate_list_dicts)))


# - - -
if __name__ == '__main__':
    app.run(debug=False)
#  - -
