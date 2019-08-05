import math
from collections import defaultdict
from QueryRunner import execute
from Config import loginInfo
import datetime
import json
import ast

'''
Input: date1 & date 2, where date1 > date2
Output: difference in hours between date1 and date2
'''
def getDiffInHours(date1, date2):
    lastRegisteredDate = datetime.datetime.strptime(str(date2), "%Y-%m-%d %H:%M:%S")
    currentDate = datetime.datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
    duration = currentDate - lastRegisteredDate
    duration_in_s = duration.total_seconds()
    hours = divmod(duration_in_s, 3600)[0]
    return int(hours)

'''
Input: Save last entry of the edge in context
Output: None
'''
def saveEntry(dictionary):
    theKey = dictionary['theKey']
    theSource = dictionary['theSource']
    theDestination = dictionary['theDestination']
    lastMaxPosition = dictionary['lastMaxPosition']
    lastTimeSeen = dictionary['lastTimeSeen']
    firstTimeSeen = dictionary['firstTimeSeen']
    lastReportedRareEdge= dictionary['lastReportedRareEdge']
    lastRareEdgePosition = dictionary['lastRareEdgePosition']
    currentValue = dictionary['currentValue']
    currentHour = dictionary['currentHour']
    expectedValue = dictionary['expectedValue']
    lastMaxValue = dictionary['lastMaxValue']
    stdDeviationInfo = json.dumps(dictionary['stdDeviationInfo'])
    query = "INSERT INTO angel_test_edges_connection_stats_snowflake VALUES ('" + str(theKey) + "','" + str(theSource) + "','" + str(theDestination) + "'," + str(lastMaxPosition) + ",'" + str(lastTimeSeen) + "','" + str(firstTimeSeen) + "'," + str(lastReportedRareEdge) + "," + str(lastRareEdgePosition) + "," + str(currentValue) + "," + str(currentHour) + "," + str(expectedValue) + "," + str(lastMaxValue) + ",'" + str(stdDeviationInfo) + "')"
    execute(query, loginInfo)
    return

'''
Input: Store Rare edge info
Output: None
'''

def saveAlert(theKey, theValue, thePosition, theDate):
    theSource, theDestination = getSourceAndDestinationFromKey(theKey)
    query = "INSERT into ANGEL_TEST_EDGES_ALERT_SNOWFLAKE values ('" + str(theKey) + "','" + str(theSource) + "','" + str(theDestination) + "'," +str(theValue) + "," + str(thePosition) + ",'"+theDate+"')"
    execute(query, loginInfo)
    return

'''
Input: key consisting of "source" + "destination".
Output: Get last entry of the edge in context
'''
def getLastEntry(key):

    # query = "SELECT theKey, theSource, theDestination, lastMaxPosition, lastTimeSeen, firstTimeSeen, lastReportedRareEdge, lastRareEdgePosition, currentValue, currentHour, expectedValue, lastMaxValue, parse_json(stdDeviationInfo) as STDDEVIATIONINFO"
    query = "SELECT * FROM angel_test_edges_connection_stats_snowflake WHERE theKey = '" + key + "' ORDER BY LASTTIMESEEN DESC LIMIT 1"
    query = "SELECT * FROM angel_test_edges_connection_stats_snowflake WHERE theKey = '" + key + "' LIMIT 1"
    result = execute(query, loginInfo)

    dictionary = getNewEntryObject(key)
    for index, row in result.iterrows():
        dictionary['theKey'] = row['THEKEY']
        dictionary['theSource'] = row['THESOURCE']
        dictionary['theDestination'] = row['THEDESTINATION']
        dictionary['lastMaxPosition'] = row['LASTMAXPOSITION']
        dictionary['lastTimeSeen'] = row['LASTTIMESEEN']
        dictionary['firstTimeSeen'] = row['FIRSTTIMESEEN']
        dictionary['lastReportedRareEdge'] = row['LASTREPORTEDRAREEDGE']
        dictionary['lastRareEdgePosition'] = row['LASTRAREEDGEPOSITION']
        dictionary['currentValue'] = row['CURRENTVALUE']
        dictionary['currentHour'] = row['CURRENTHOUR']
        dictionary['expectedValue'] = row['EXPECTEDVALUE']
        dictionary['lastMaxValue'] = row['LASTMAXVALUE']
        dictionary['stdDeviationInfo'] = row['STDDEVIATIONINFO']

    return dictionary


'''
Input: One hour range, start and end, currently generated automatically.
Output: Existing edges with # of connections during given time frame in the format:
        Dictionary[key] = [source, destination, #connection]
'''
def getEdges(fromDate, toDate):

    query = "SELECT ZEROIFNULL(sum(edge_t.props:num_conns)) num_conns," \
    " CONCAT(split_part(ns.props:exe_path, '/', -1),'',ns.props:cmdline_terms[0]) as sourceApplication," \
    " CONCAT(split_part(nd.key:hostname, '.', -2), split_part(nd.key:hostname, '.', -1), nd.key:ip_internal, nd.key:port, nd.key:protocol) as destinationDNS" \
    " FROM GRAPH_INTERNAL.edge_t, GRAPH_INTERNAL.node_t ns, GRAPH_INTERNAL.node_t nd" \
    " WHERE edge_t.SRC_KEY = ns.KEY" \
    " AND edge_t.DST_KEY = nd.KEY AND edge_t.start_time = ns.start_time  AND edge_t.start_time = nd.start_time" \
    " AND edge_t.start_time >= to_timestamp('%s') AND edge_t.start_time < to_timestamp('%s')" \
    " AND ns.start_time >= to_timestamp('%s') AND ns.start_time < to_timestamp('%s')" \
    " AND nd.start_time >= to_timestamp('%s') AND nd.start_time < to_timestamp('%s')" \
    " AND edge_t.SRC_TYPE = 'Process'" \
    " AND edge_t.DST_TYPE = 'DnsSep'" \
    " AND sourceApplication = 'nginxworker'" \
    " AND destinationDNS = 'snowflakecomputingcom080TCP'" \
    " GROUP BY sourceApplication, destinationDNS;" % (
    fromDate, toDate, fromDate, toDate, fromDate, toDate)


    # Create a custom dictionary w/ format [key] = [source, destination, #connection] from the result
    result = execute(query, loginInfo)
    dictionary = defaultdict(int)
    for index, row in result.iterrows():
        source, destination, num_con = row['SOURCEAPPLICATION'], row['DESTINATIONDNS'], int(row['NUM_CONNS'])
        dictionary[getKeyFromSourceAndDestination(source, destination)] = [source, destination, num_con]
    return dictionary



'''

Input: Params needed for variance computation
Output: Computed Std Dev (stdDev) & Values stored for next computation (object)
Source: Adapted from https://blog.rapid7.com/2016/10/19/overview-of-online-algorithm-using-standard-deviation-example/
'''
def processNextStdDev(entry, tick):
    object = dict()
    entry = ast.literal_eval(entry) # string to dict
    object['count'] = entry['count'] + 1
    object['mean'] = entry['mean'] + (tick - entry['mean']) / entry['count']
    object['sum'] = entry['sum'] + (tick - entry['mean']) * (tick - object['mean'])
    object['variance'] = object['sum'] / entry['count']
    stdDev = math.sqrt(object['variance']) if entry['count'] > 0 else 0
    object['stdDev'] = stdDev
    return object, stdDev

'''
Default stdDeviationInfo object
'''
def getNewStdDevObject():
    object = dict()
    object['count'] = 1.0
    object['mean'] = 0.0
    object['sum'] = 0.0
    object['variance'] = 0.0
    object['stdDev'] = 0.0
    return object

'''
Default Entry object
'''
def getNewEntryObject(key):
    object = {}
    object['theKey'] = key
    object['theSource'], object['theDestination'] = getSourceAndDestinationFromKey(key)
    object['lastMaxPosition'] = 0
    object['lastTimeSeen'] = 0
    object['firstTimeSeen'] = 0
    object['lastReportedRareEdge'] = 0
    object['lastRareEdgePosition'] = 0
    object['currentValue'] = 0
    object['currentHour'] = 0
    object['expectedValue'] = 0
    object['lastMaxValue'] = 0
    object['stdDeviationInfo'] = str(getNewStdDevObject())  # str parse needed for entry = ast.literal_eval(entry)
    return object

'''
Input: Key as {source}---{destination}
Output: Source, Destination
'''
def getSourceAndDestinationFromKey(theKey):
    return theKey.split("---")[0], theKey.split("---")[1]

'''
Input:  Source, Destination
Output: Key as the concatenation of {source}---{destination}
'''
def getKeyFromSourceAndDestination(source, destination):
    return source + '---' + destination


'''
Input: Current Hour, Key
Output: Print when mark is reached just for debugging purpose
'''
def printForDebug(currentHour, key):
    if currentHour == 1000:
        print("One Thousand")
        print('Analyzing ', key, currentHour)
    if currentHour == 2000:
        print("Two Thousand")
        print('Analyzing ', key, currentHour)
    if currentHour == 3000:
        print("Three Thousand")
        print('Analyzing ', key, currentHour)
    if currentHour == 4000:
        print("Four Thousand")
        print('Analyzing ', key, currentHour)
    if currentHour == 5000:
        print("Five Thousand")
        print('Analyzing ', key, currentHour)

