# New:

## The table angel_test_monitored_edges contains the edges to be monitored (i.e. source, destination).
## The table angel_test_edges_connection_stats contains the stats for each of the monitored edges (i.e. source, destination, startpoint, stats, data).
## So far, we analyzed one edge at the time. However, now, the idea now is to analyze all possible edges in the range of 6 months. For this, we analyze all edges except the ones with source “wget”, this reduces the number of edges to be analyzed from 340,015 to 599 (PREPROD_CDB_PREPROD_9593B140CA75F1259DD584236657F2A996A6FA2A14B603FF) and from 340,015 to 599 (PREPROD_CDB_SNOWFLAKE_E6FB97EF9C0EFB48D1AA880139F22303).
## It was fine to analyze a few edges with Jupiter Notebook, however, when a considerable amount of edges are concurrently analyzed, Jupiter Notbook does not work properly. Thus, we set up our project and started testing with Pycharm.
## The parameters were the source, the destination, and the starting time and ending time. Now, the parameters are only the starting and ending time (e.g. one hour range) and all edges in the time-frame are analyzed.


# Next Steps:

## Finish migrating project to pycharm
## Run tests in pre-prod and snowflake
## Create a table to save the stats, currently it is saved in memory
## Update this document
