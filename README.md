# Burma Prices data warehouse

## About 
This repo is based on my personal [Burma Prices Monitoring Project](burma-prices.leetdev.net). I would like to build local/cloud data warehouse system to maintain IN/OUT data flows of the project.

## Tools to use
1. DBT
    - To combine sqlite db into one single price database 
    - To select only necessary columns and data values.
    - To understand data schemas of overall Prices monitoring project.
2. ETL Tool
    - Not decided yet (June 22)
    - Airflow or Trino

## Requirements
- dbt-sqlite

## List to do
- [ ] Connect SQLite db files with DBT
- [ ] Connect with Google Big Query for Rice price data.

------------
#### Develop
- This project is dedicated to help for the growth of Burma Open Data community.
- Code by @GmGniap