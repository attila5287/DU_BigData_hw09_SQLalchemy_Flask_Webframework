from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import sqlalchemy
from flask import Flask, jsonify
import datetime as dt
import numpy as np
#  - -
# - SQLalchemy to reflect database from SQLite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Flask setup
app = Flask(__name__)


# @app.route('/api/v1.0/<start>/<end>')


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
    # return jsonify(list(np.ravel(endstartdate_list_dicts)))
    return endstartdate_list_dicts


#
print('\n TEST \n======\n')
output_test = temps_MinAvgMax_startenddates('2017-07-08', '2017-07-18')
print(output_test)
