import pandas as pd
from api_app.db_manager import DbManager
from datetime import datetime

backup_table = input("Enter backup table name: ")
engine = DbManager().get_engine()

## Get table names from postgresql
available_tables = DbManager().get_all_table_names()

def read_table(table_name, eng=engine):
    table_df = pd.read_sql_table(
        table_name,
        con= eng,
    )
    return table_df

if backup_table in available_tables:
    backup_t = read_table(backup_table)
    today_date = datetime.now().date().strftime("%Y-%m-%d")
    backup_t.to_csv(f'./backup/{backup_table}_{today_date}.csv',index=False)
else:
    print(f"No table found : {backup_table}")

