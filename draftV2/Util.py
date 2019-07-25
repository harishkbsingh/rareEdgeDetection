from collections import defaultdict
from DataImporter import dataImporter
from Config import monitoredEdgesTable, loginInfo

def getMonitoredEdges():
    query = "SELECT * FROM " + monitoredEdgesTable + ";"
    result = dataImporter(query, loginInfo)
    registeredEdges = []

    for index, row in result.iterrows():
        registeredEdges.append([row['SOURCEAPPLICATION'], row['DESTINATIONDNS']])
    return registeredEdges


def getEdges(start, end):

    fromDate = start
    toDate = end
    but = 'wget%'

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
            " AND sourceApplication NOT LIKE '%s'" \
            " GROUP BY sourceApplication, destinationDNS;" % (
            fromDate, toDate, fromDate, toDate, fromDate, toDate, but)

    result = dataImporter(query, loginInfo)
    dictionary = defaultdict(int)

    # fill with 0
    monitoredEdges = getMonitoredEdges()
    for source, destination in monitoredEdges:
        key = source + '---' + destination
        dictionary[key] = [source, destination, 0]

    # update valid positions
    for index, row in result.iterrows():
        key = row['SOURCEAPPLICATION'] + '---' + row['DESTINATIONDNS']
        dictionary[key] = [row['SOURCEAPPLICATION'], row['DESTINATIONDNS'], int(row['NUM_CONNS'])]
    return dictionary
