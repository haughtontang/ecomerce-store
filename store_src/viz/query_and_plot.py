import sqlite3
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from store_src.sql.upload_data_to_db import return_conn_and_cursor_obj_for_table

"""
- I gave ChatGPT some examples of the data in my SQL db and asked it for 10 questions that I can query the db with
- They are: 
    Total Sales by Artist:
        - "Can you provide the total sales for each artist?"
        - "Who are the top 5 artists based on billboard rating?"
            - This is kind of done since I limited the data to the top 10
        - "What is the average album sales across all artists?"
        - "Which artists have more than 1 million streaming followers?"
        - "Can you compare the total sales and album sales for each artist?"
        - "Can you show the latest concert revenue for each artist?"
        - "How many songs does each artist have?"
        - "Is there a correlation between streaming followers and total sales?"
        - "How do total sales vary over the latest album release dates?"
        - "Which artists have released the most albums?"
"""


def plot_total_sales_per_artist(database_path: Path, table_name: str, output_path: Path):
    # Since there are 200 artists and this would make a messy plot, I am going to modify the question to only include the top 10 billboard artists
    conn, cur = return_conn_and_cursor_obj_for_table(database_path=database_path)
    cur.execute(f"SELECT artist, total_sales, billboard_rating FROM {table_name} ORDER BY billboard_rating ASC LIMIT 10;")
    query_data = cur.fetchall()
    x = np.arange(len(query_data))
    y = [row[1] for row in query_data]
    x_labels = [row[0] for row in query_data]
    fig, ax = plt.subplots()
    ax.bar(x, y, color="#4EA5EB")
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    ax.set_xlabel('Artist')
    ax.set_ylabel('Total Sales')
    ax.set_title('Total Sales by Artist')
    ax.spines[['right', 'top']].set_visible(False)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    conn.close()


def print_avg_album_sales_for_all_artists(database_path: Path, table_name: str):
    conn, cur = return_conn_and_cursor_obj_for_table(database_path=database_path)
    cur.execute(f"SELECT album_sales FROM {table_name};")
    query_data = cur.fetchall()
    print(f"Avg Album sales across all artists: {np.mean(query_data)}")


def print_artists_with_more_than_one_million_followers(database_path: Path, table_name: str):
    conn, cur = return_conn_and_cursor_obj_for_table(database_path=database_path)
    cur.execute(f"SELECT artist FROM {table_name} WHERE streaming_followers > 1000000;")
    query_data = cur.fetchall()
    print(f"Number of artists with more than one million followers: {len(query_data)}\n"
          f"Artists with > one million followers: {[i[0] for i in query_data]}")


def compare_album_and_total_sales_for_top_10(database_path: Path, table_name: str, output_path: Path):
    conn, cur = return_conn_and_cursor_obj_for_table(database_path=database_path)
    cur.execute(f"SELECT artist, total_sales, album_sales FROM {table_name} ORDER BY billboard_rating ASC LIMIT 10;")
    query_data = cur.fetchall()

    bar_width = 0.3
    x1 = np.arange(len(query_data))
    x2 = [x + bar_width for x in x1]
    y1 = [row[1] for row in query_data]
    y2 = [row[2] for row in query_data]
    x_labels = [row[0] for row in query_data]

    fig, ax = plt.subplots()
    bars1 = ax.bar(x1, y1, color="#4EA5EB", width=bar_width, label='Total Sales')
    bars2 = ax.bar(x2, y2, color='lightcoral', width=bar_width, label='Album Sales')

    ax.set_xlabel('Artist')
    ax.set_ylabel('Sales')
    ax.set_title('Total Sales vs Album Sales by Artist')
    ax.set_xticks([i + bar_width / 2 for i in x1])
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    ax.legend()
    ax.spines[['right', 'top']].set_visible(False)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    conn.close()


def plot_artists_with_the_most_albums(database_path: Path, table_name: str, output_path: Path):
    conn, cur = return_conn_and_cursor_obj_for_table(database_path=database_path)
    cur.execute(f"SELECT artist, number_of_albums FROM {table_name} ORDER BY number_of_albums DESC LIMIT 5;")
    query_data = cur.fetchall()

    x = np.arange(len(query_data))
    y = [row[1] for row in query_data]
    x_labels = [row[0] for row in query_data]
    fig, ax = plt.subplots()
    ax.bar(x, y, color="#4EA5EB")
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    ax.set_xlabel('Artist')
    ax.set_ylabel('Number of Albums')
    ax.set_title('Number of Albums by Artist')
    ax.spines[['right', 'top']].set_visible(False)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    conn.close()


if __name__ == '__main__':
    table_name = "billboard_artists"
    db_path = Path(f"/Users/donhaughton/Documents/PycharmProjects/ecommerce-store/data/{table_name}.db")
    output_dir = Path(f"/Users/donhaughton/Documents/PycharmProjects/ecommerce-store/data/query_plots")

    plot_total_sales_per_artist(database_path=db_path, table_name=table_name, output_path=output_dir.joinpath("top_10_sales.png"))
    print_avg_album_sales_for_all_artists(database_path=db_path, table_name=table_name)
    print_artists_with_more_than_one_million_followers(database_path=db_path, table_name=table_name)
    compare_album_and_total_sales_for_top_10(database_path=db_path, table_name=table_name,
                                             output_path=output_dir.joinpath("top10_album_vs_total_sales.png"))
    plot_artists_with_the_most_albums(database_path=db_path, table_name=table_name,
                                      output_path=output_dir.joinpath("artist_by_album_number.png"))
