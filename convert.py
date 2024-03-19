import sqlite3
import json


def convert_sqlite_to_json(sqlite_file):
    # Connect to SQLite database
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()

    # Get list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    data = {}

    # Iterate over each table
    for table in tables:
        table_name = table[0]

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # # Convert rows to dictionary
        table_data = []
        for row in rows:
            row_dict = {}
            for i, column in enumerate(cursor.description):
                row_dict[column[0]] = row[i]
            table_data.append(row_dict)

        # # Add table data to main data dictionary
        data[table_name] = table_data

    # Close the connection to the database
    conn.close()

    return json.dumps(data, indent=4)


if __name__ == "__main__":
    # sqlite_file = input("Enter the SQLite file path: ")
    sqlite_file = "./dua_main.sqlite"
    json_data = convert_sqlite_to_json(sqlite_file)
    with open("output.json", "w") as outfile:
        outfile.write(json_data)
    print("Conversion successful. JSON file saved as output.json")
