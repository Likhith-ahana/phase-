from sqlalchemy import text

from app.database.connection import engine


try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database(), version()")
        )

        database_name, database_version = result.fetchone()

        print("Database connection successful!")
        print("Database:", database_name)
        print("Version:", database_version)

except Exception as error:
    print("Database connection failed!")
    print("Error:", error)