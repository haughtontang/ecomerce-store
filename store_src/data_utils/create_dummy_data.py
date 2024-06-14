from store_src.data_utils.bs_data_pull import billboard_200_scraper
import numpy as np
from datetime import datetime
import json
from pathlib import Path
import random
import string


def write_json(output_path: Path, data):
    with output_path.open('w') as json_file:
        json.dump(data, json_file, indent=2)


def generate_random_key(length: int = 5) -> str:
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def generate_dummy_data(output_path: Path):
    output_list = list()
    album_data = billboard_200_scraper()
    for idx, artist_dict in enumerate(album_data):
        latest_album = artist_dict["album_title"]
        artist = artist_dict["artist"]
        total_sales = np.random.randint(10000, int(1e9))
        album_sales = np.random.randint(10000, int(1e9))
        streaming_followers = np.random.randint(10000, int(1e6))
        latest_concert_revenue = np.random.random() * 1000000
        latest_album_release_date = str(datetime(year=np.random.randint(2000, 2024),
                                                 month=np.random.randint(1, 12),
                                                 day=np.random.randint(1, 30)))
        number_of_songs = np.random.randint(1, 200)
        number_of_albums = np.random.randint(1, 10)
        output_list.append({"artist_id": generate_random_key(length=5), "artist": artist, "billboard_rating": idx + 1,
                            "latest_album": latest_album, "total_sales": total_sales, "album_sales": album_sales,
                            "streaming_followers": streaming_followers, "latest_concert_revenue": latest_concert_revenue,
                            "latest_album_release_date": latest_album_release_date, "number_of_songs": number_of_songs,
                            "number_of_albums": number_of_albums})
    write_json(output_path=output_path, data=output_list)


if __name__ == '__main__':
    generate_dummy_data(output_path=Path("~/Documents/PycharmProjects/ecommerce-store/data/dummy_billboard_artist_data.json").expanduser())
