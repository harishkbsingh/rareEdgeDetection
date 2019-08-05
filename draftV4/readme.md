## To Run:
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



## TODO Optimization:
- Running a test on the edge "nginxworker" (source application) to "snowflakecomputingcom080TCP" (dns destination) for 6 months took 27935.60666704178 seconds, which is 7.75 hours. 


## Next Steps (Missing):

1. Test with all edges for Snowflake and PreProd

2. Update documentation

3. Java implementation?
