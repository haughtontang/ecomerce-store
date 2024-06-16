import sqlite3
from pathlib import Path
from store_src.data_utils.create_dummy_data import load_json


def return_conn_and_cursor_obj_for_table(database_path: Path) -> (sqlite3.Connection, sqlite3.Cursor):
    conn = sqlite3.connect(database_path.as_posix())
    return conn, conn.cursor()


def create_table_and_upload_data(table_name: str, database_path: Path, data_path: Path):
    data = load_json(data_path=data_path)
    conn, cur = return_conn_and_cursor_obj_for_table(database_path=database_path)
    # Create the artists table
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            artist_id TEXT PRIMARY KEY,
            artist TEXT NOT NULL,
            billboard_rating INTEGER NOT NULL,
            latest_album TEXT NOT NULL,
            total_sales INTEGER NOT NULL,
            album_sales INTEGER NOT NULL,
            streaming_followers INTEGER NOT NULL,
            latest_concert_revenue REAL NOT NULL,
            latest_album_release_date TEXT NOT NULL,
            number_of_songs INTEGER NOT NULL,
            number_of_albums INTEGER NOT NULL
        )
    ''')

    # Insert data into the artists table
    for entry in data:
        cur.execute(f'''
            INSERT INTO {table_name} (
                artist_id, artist, billboard_rating, latest_album, total_sales, album_sales,
                streaming_followers, latest_concert_revenue, latest_album_release_date,
                number_of_songs, number_of_albums
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry['artist_id'], entry['artist'], entry['billboard_rating'], entry['latest_album'],
            entry['total_sales'], entry['album_sales'], entry['streaming_followers'],
            entry['latest_concert_revenue'], entry['latest_album_release_date'],
            entry['number_of_songs'], entry['number_of_albums']
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database setup and data insertion complete.")


if __name__ == '__main__':
    table_name = "billboard_artists"
    create_table_and_upload_data(table_name=table_name,
                                 database_path=Path(f"/Users/donhaughton/Documents/PycharmProjects/ecommerce-store/data/{table_name}.db"),
                                 data_path=Path("/Users/donhaughton/Documents/PycharmProjects/ecommerce-store/data/dummy_billboard_artist_data.json"))
