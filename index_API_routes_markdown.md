<dd><dl><br><h2>Available Routes:<h2></dl></dd>
        <h4>/api/v1.0/stations<br/></h4>
        <dd> *  lists the stations and their observation codes</dd> 
        <h4><br>/api/v1.0/tobs</h4>
        <dd> *  finds the most recent date on the dataset and brings the last twelve months Temperature observation data with units in Fahrenheit </dd> 
        <h4>/api/v1.0/precipitation<br/></h4>
        <dd> *  finds the most recent date on the dataset and brings the last twelve months Precipitation observation data with units in inches</dd>
        <h4>/api/v1.0/<start></h4>
        <dd> *  start date- via API request- required at the end of the url</dd>
        <dd> *  calculates Minimum, Average and Maximum Temperature values </dd> 
        <dd> *  displays a json format list with  above temp values</dd>
        <h4>/api/v1.0/<start>/<end></h4>
        <dd> *  start and end dates separated by a slash / required at the end of the url via api request</dd><br/>