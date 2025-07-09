import os
import snowflake.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_snowflake_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        database="SNOWFLAKE",
        schema="ACCOUNT_USAGE"
    )

def get_query_history(days=3):
    query = f"""
    SELECT USER_NAME, QUERY_TEXT, EXECUTION_STATUS,
           TOTAL_ELAPSED_TIME / 1000 AS DURATION_SEC,
           CREDITS_USED_CLOUD_SERVICES,
           START_TIME
    FROM QUERY_HISTORY
    WHERE START_TIME > DATEADD('day', -{days}, CURRENT_TIMESTAMP())
    ORDER BY DURATION_SEC DESC
    LIMIT 50;
    """
    conn = get_snowflake_connection()
    return pd.read_sql(query, conn)

def get_warehouse_utilization():
    query = """
    SELECT 
        WAREHOUSE_NAME,
        SUM(CREDITS_USED) AS TOTAL_CREDITS,
        DATE_TRUNC('hour', START_TIME) AS HOUR
    FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
    WHERE START_TIME > DATEADD('day', -3, CURRENT_TIMESTAMP())
    GROUP BY WAREHOUSE_NAME, DATE_TRUNC('hour', START_TIME)
    ORDER BY HOUR DESC
    """
    conn = get_snowflake_connection()
    return pd.read_sql(query, conn)





def estimate_cost_savings(query_df, wh_df):
    # Estimate 30% saving on top 5 longest queries
    top_queries = query_df.head(5)
    total_credits_used = top_queries['CREDITS_USED_CLOUD_SERVICES'].sum()
    potential_saved_credits = total_credits_used * 0.3

    # Estimate warehouse waste where total usage is low
    underused_wh = wh_df.groupby("WAREHOUSE_NAME")["TOTAL_CREDITS"].sum().reset_index()
    low_credit_wh = underused_wh[underused_wh["TOTAL_CREDITS"] < 1.0]  # less than 1 credit in 3 days
    idle_credits = low_credit_wh["TOTAL_CREDITS"].sum() * 0.25  # assume 25% waste

    return round(potential_saved_credits + idle_credits, 2)



