from collections import defaultdict
from DataImporter import dataImporter
from Config import loginInfo
import datetime

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
Input: Info related to edge in context
Output: None
'''
def saveStat(dictionary):
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
    stdDeviation = dictionary['stdDeviation']
    query = "INSERT INTO angel_test_edges_connection_stats_snowflake VALUES ('" + str(theKey) + "','" + str(theSource) + "','" + str(theDestination) + "'," + str(lastMaxPosition) + ",'" + str(lastTimeSeen) + "','" + str(firstTimeSeen) + "'," + str(lastReportedRareEdge) + "," + str(lastRareEdgePosition) + "," + str(currentValue) + "," + str(currentHour) + "," + str(expectedValue) + "," + str(lastMaxValue) + "," + str(stdDeviation) + ")"
    dataImporter(query, loginInfo)
    return

'''
Input: Rare edge info
Output: None
'''
def saveAlert(theKey, theValue, thePosition, theDate):
    theSource, theDestination = theKey.split("---")[0], theKey.split("---")[1]
    query = "INSERT into ANGEL_TEST_EDGES_ALERT_SNOWFLAKE values ('" + str(theKey) + "','" + str(theSource) + "','" + str(theDestination) + "'," +str(theValue) + "," + str(thePosition) + ",'"+theDate+"')"
    dataImporter(query, loginInfo)
    return

'''
Input: key consisting of "source" + "destination".
Output: Latest info related to edge in context
'''
def getStat(key):
    query = "SELECT * FROM angel_test_edges_connection_stats_snowflake WHERE theKey = '" + key + "' ORDER BY LASTTIMESEEN DESC LIMIT 1"
    result = dataImporter(query, loginInfo)
    dictionary = defaultdict(int)
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
        dictionary['stdDeviation'] = row['STDDEVIATION']
    return dictionary


'''
Input: One hour range, start and end, currently generated automatically.
Output: Existing edges with # of connections during given time frame in the format:
        Dictionary[key] = [source, destination, #connection]
'''
def getEdges(fromDate, toDate):

    # but = 'wget%'
    # " AND sourceApplication NOT LIKE '%s'" \
    # " AND sourceApplication = 'nginxworker'" \
    # " AND destinationDNS = 'snowflakecomputingcom080TCP'"

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
            " AND sourceApplication != 'NULL'" \
            " AND destinationDNS != 'NULL'" \
            " GROUP BY sourceApplication, destinationDNS;" % (
            fromDate, toDate, fromDate, toDate, fromDate, toDate)


    # Given a Snowflake dataset "result"
    # Create a custom dictionary in the format Dictionary[key] = [source, destination, #connection]
    result = dataImporter(query, loginInfo)
    dictionary = defaultdict(int)
    for index, row in result.iterrows():
        dictionary[row['SOURCEAPPLICATION'] + '---' + row['DESTINATIONDNS']] = [row['SOURCEAPPLICATION'], row['DESTINATIONDNS'], int(row['NUM_CONNS'])]
    return dictionary

'''
Input: source & destination
Output: key created by concatenating source & dest
'''
def getKey(source, destination):
    return source + '---' + destination

'''
Input: Current Hour, Key
Output: Printing when mark is reached just for debugging purpose
'''
def printing(currentHour, key):
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