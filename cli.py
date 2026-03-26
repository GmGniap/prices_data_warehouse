import argparse
from api_app.db_manager import DbManager

def main():
    parser = argparse.ArgumentParser(description="Database Administration CLI")
    parser.add_argument('--init-db', action='store_true', help='Initiate database/create tables if they do not exist')
    parser.add_argument('--reset', action='store_true', help='Reset all tables (drop and recreate) or specific table via --table_name')
    parser.add_argument('--truncate', action='store_true', help='Truncate all tables (delete data inside) or specific table via --table_name')
    parser.add_argument('--table_name', type=str, help='Specific table name for reset or truncate')
    parser.add_argument('--health', action='store_true', help='Check database health securely')
    parser.add_argument('--local', action='store_true', help='Use local SQLite database connection instead of defined cloud configuration')
    
    args = parser.parse_args()

    # If no functional arguments provided, print help
    if not any([args.init_db, args.reset, args.truncate, args.health]):
        parser.print_help()
        return

    print(f"Connecting to {'LOCAL SQLITE' if args.local else 'CLOUD POSTGRESQL'} database...")
    try:
        db = DbManager(use_local=args.local)
    except Exception as e:
        print(f"Failed to initialize Database Manager: {e}")
        return

    if args.health:
        db.check_health()
    
    if args.init_db:
        print("Initializing Database tables...")
        db.create_tables()

    if args.reset:
        if args.table_name:
            print(f"Resetting table: {args.table_name}")
            db.reset_tables(table_name=args.table_name)
        else:
            print("Resetting all tables...")
            db.reset_tables()

    if args.truncate:
        if args.table_name:
            print(f"Truncating table: {args.table_name}")
            db.truncate_tables(table_name=args.table_name)
        else:
            print("Truncating all tables...")
            db.truncate_tables()

if __name__ == "__main__":
    main()
