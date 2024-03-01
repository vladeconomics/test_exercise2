
#############################
########## SQL + pandas ##########
from sqlalchemy import create_engine, text
import pandas as pd

# Create a connection using SQLAlchemy
connection_string = (
    "mssql+pyodbc://@A01-DBAAS.local,12345/ESM_DBA_ABC?"
    "driver=ODBC+Driver+17+for+SQL+Server&"
    "trusted_connection=yes" 
)
engine = create_engine(connection_string)
sql_query = """
WITH h AS (                             
    SELECT [id]                         
          ,[entity]
          ,[country]
          ,[z]
          ,[report_date]
          ,[market_value_eur]
    FROM [T1].[S1].[H2] 
    WHERE (entity = 'ABC' AND report_date > '2010-01-01' )
    AND (country LIKE '%France%') 
)
SELECT * 
FROM h
LEFT JOIN (SELECT id, col1, col2 FROM [T1].[S1].[H3]) as o
ON h.[id] = o.[id];
"""
df = pd.read_sql(sql_query, engine)
print(df.head()) 

gdf = df.groupby(['entity','report_date']).agg({'market_value_eur':'sum'}).reset_index()
gdf["report_date"] = pd.to_datetime(gdf["report_date"], format='%Y-%m-%d')
