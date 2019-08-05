## Rare Edge Detection

### Description

A time series is an ordered sequence of values at equally spaced time intervals. There are several popular algorithms to detect rareness in time series, however, due to the number of considerations and nuances involved in our domain, we opted to develop tailored algorithm.

In this work, our goal is to create an algorithm to help us detect “rare edges” between two (entity) instances  by analyzing the behavior on the number of connection between the entities in context.

The overall algorithm can be summarized as follows:

> 1. Take as input initial time. 

> 2. For the given time frame, we analyze each of the existent edges.   
   2.1 Persist the metrics used determined during the analysis on the table “angel_test_edges_connection_stats”, these are used for online learning.


To analyze each of the existent edges, we use the following approach:

> 1. During the training period (first 30 days), we obtain the entry with the most number of connections. This value and the cumulative std serve to compute the next expected number of connection for each of the edges.

> 2. After the training period, we continue updating each of the edge’s stats. Our two key heuristics are: (a) There cannot be two rare edges within 24 hours; (b) The expected number of connection of each of the edges decreases throughout the time. For this, we used a custom linear regression function created using least squares fitting.

<br/>

### How to Run ?

1. Add config file
    ```
    Config.py

        # Constant
        trainingTime =  30 * 24
        oneDayAsMinTime = 24

        # Example for Snowflake
        loginInfo = ['dev_angel', 'lwdev', 'DEV_TEST',
                     'PREPROD_CDB_SNOWFLAKE_E6FB97EF9C0EFB48D1AA880139F22303', 'GRAPH_INTERNAL',
                     'password']
        ```
2. Run Main.py

<br/>

### Top-level directory layout

    .
    ├── Main                    # Start point: runs the algorithm for a range of dates
    ├── QueryRunner             # Query executor helper class
    ├── Algorithm               # Core algorithm
    ├── Util                    # Tools and utilities
    ├── Config                  # General config
    └── README.md
    
    
### Methods Short Description:
    .
    ├── Main
    │   ├── runMonthsSimulation # Run algorithm for long time frame (6 months in this case).
    │   └── runAlgorithm        # For each edge in the time frame, the algorithm is executed
    ├── QueryRunner
    │   └── execute             # Receives credentials and query to be executed in Snowflake.
    ├── Algorithm               
    │   ├── decayFunction       # Use least squares fittings to compute expected value decrease.
    │   └── feed                # Process edge in context in current time frame (hour).
    └── Util
        ├── getDiffInHours          # difference in hours between input dates.
        ├── saveEntry               # Save last entry of the edge in context.
        ├── saveAlert               # Store Rare edge info.
        ├── getLastEntry            # Get last entry of the edge in context.
        ├── getEdges                # Return existing edges with # of connections during given time frame in the format.
        ├── processNextStdDev       # Compute Std Dev (stdDev) & Values stored for next computation (object).
        ├── getNewStdDevObject      # Default stdDeviationInfo object.
        ├── getNewEntryObject       # Default Entry object
        └── printForDebug           # Print when mark is reached just for debugging purpose.
    
<br/>

### In Progress

> Optimization: Running a test on the edge "nginxworker" (source application) to "snowflakecomputingcom080TCP" (dns destination) for 6 months took 27935.60666704178 seconds, which is 7.75 hours. 

<br/>

### Next Steps (Missing)

1. Test with all edges for Snowflake and PreProd

2. Update THIS documentation

3. Java implementation?
