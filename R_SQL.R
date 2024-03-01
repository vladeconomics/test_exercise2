
library(DBI)
library(dplyr)

connection_string <- "Driver={ODBC Driver 17 for SQL Server};Server=A23-DBAAS.local,12345;Database=DBB_DB12_MKT;Trusted_Connection=Yes;"
con <- dbConnect(odbc::odbc(), .connection_string = connection_string)

sql_query <- "
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
"
df <- dbGetQuery(con, sql_query)

gdf <- df %>%
  group_by(entity, report_date) %>%
  summarise(market_value_eur = sum(market_value_eur)) %>%
  mutate(report_date = as.Date(report_date, format='%Y-%m-%d'))

print(head(gdf))
