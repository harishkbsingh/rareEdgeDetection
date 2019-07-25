import pandas as pd
import sys
import snowflake.connector

def dataImporter(query, loginInfo):
    # Get the other login info etc. from the command line.
    loginParams = ['user', 'account', 'warehouse', 'database', 'schema', 'password']

    if all(param in loginInfo for param in loginParams) and isinstance(loginInfo, dict):
        USER = loginInfo['user']
        ACCOUNT = loginInfo['account']
        WAREHOUSE = loginInfo['warehouse']
        DATABASE = loginInfo['database']
        SCHEMA = loginInfo['schema']
        PASSWORD = loginInfo['password']

    elif isinstance(loginInfo, list) and len(loginInfo) == 6:
        USER = loginInfo[0]
        ACCOUNT = loginInfo[1]
        WAREHOUSE = loginInfo[2]
        DATABASE = loginInfo[3]
        SCHEMA = loginInfo[4]
        PASSWORD = loginInfo[5]

    else:
        print("\nError: You must either pass the params\n   ", loginParams,
              "\nas the dict loginInfo or IN ORDER as a list or IN ORDER as command-line arguments.")
        print("\nCheck that your keys match case as the above if using the dict.")
        sys.exit(-1)

    con = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        warehouse=WAREHOUSE,
        database=DATABASE,
        schema=SCHEMA
    )
    cursor = con.cursor()
    try:
        cursor.execute(query);
        df = pd.DataFrame.from_records(iter(cursor), columns=[x[0] for x in cursor.description])
        return df
    finally:
        cursor.close()