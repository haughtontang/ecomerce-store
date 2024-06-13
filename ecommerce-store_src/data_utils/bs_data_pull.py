import requests
from bs4 import BeautifulSoup


def billboard_200_scraper():
    # URL for the Billboard 200 chart
    URL = "https://www.billboard.com/charts/billboard-200/"

    # Send a GET request to the URL
    response = requests.get(URL)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        albums = []

        # Find all chart items
        chart_items = soup.find_all('li', class_='o-chart-results-list__item')

        for item in chart_items:
            # Extract the title and artist
            title_element = item.find('h3', class_='c-title')
            artist_element = item.find('span', class_='c-label')

            if title_element and artist_element:
                title = title_element.get_text(strip=True)
                artist = artist_element.get_text(strip=True)
                albums.append({'album_title': title, 'artist': artist})

        # Print the results
        for album in albums:
            print(f"Title: {album['album_title']}, Artist: {album['artist']}")
    else:
        print("Failed to retrieve the webpage.")


if __name__ == '__main__':
    billboard_200_scraper()