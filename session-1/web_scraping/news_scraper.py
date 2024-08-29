import os
PYPPETEER_CHROMIUM_REVISION = '1263111'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

import datetime
from requests_html import HTMLSession
from mysql.connector import Error
from data_connection import create_data_connection
from insert_news import (execute_query,
                         insert_reporter,
                         get_reporter_id,
                         insert_category,
                         get_category_id,
                         insert_news,
                         get_news_id,
                         insert_publisher,
                         get_publisher_id,
                         insert_image)


def process_and_insert_news_data(connection, publisher_website, publisher, title, reporter, news_datetime, category, news_body, images, url):
    try:
        # Insert category if not exists
        category_id = insert_category(connection, category, f"{category}")
        c_id = get_category_id(connection, category)
        
        # Insert reporter if not exists
        reporter_id = insert_reporter(connection, reporter, f"{reporter}@{publisher_website}")
        r_id = get_reporter_id(connection, reporter)
        
        # Insert publisher as a placeholder (assuming publisher is not provided)
        publisher_id = insert_publisher(connection, publisher, f"{publisher_website}")
        p_id = get_publisher_id(connection, publisher)
        
        # Insert news article
        news_id = insert_news(connection, c_id, r_id, p_id, news_datetime, title, news_body, url)
        n_id = get_news_id(connection, title)
        
        # Insert images
        for image_url in images:
            image_id = insert_image(connection, n_id, image_url)
    
    except Error as e:
        print(f"Error while processing news data - {e}")


def single_news_scraper(url):
    session = HTMLSession()
    try:
        response = session.get(url)
        response.html.render()  # This will download Chromium if not found

        publisher_website = url.split('/')[2] if len(url.split('/')) > 2 else None
        publisher = publisher_website.split('.')[-3] if publisher_website else None

        title = response.html.find('h3', first=True).text if response.html.find('h3') else None
        reporter = response.html.find('h4.font-bold.text-xl', first=True).text if response.html.find('h4.font-bold.text-xl') else None

        category_element = response.html.find('div.mb-2.flex.items-center.mb-4', first=True)
        category = category_element.find('a', first=True).text if category_element else None
        
        news_body = '\n'.join([p.text for p in response.html.find('p')])

        img_tags = response.html.find('img')
        images = [img.attrs['src'] for img in img_tags if 'src' in img.attrs]

        # Check if all necessary elements are found
        if all([publisher_website, publisher, title, reporter, category, news_body, images]):
            return publisher_website, publisher, title, reporter, category, news_body, images
        else:
            print(f"Failed to find all necessary elements on the webpage: {url}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    conn = create_data_connection()
    if conn is not None:
        url = "https://thefinancialexpress.com.bd/page/economy/bangladesh"
        result = single_news_scraper(url)
        if result:
            publisher_website, publisher, title, reporter, category, news_body, images = result
            print(publisher_website, publisher, title, reporter, category, news_body, images)
            process_and_insert_news_data(conn, publisher_website, publisher, title, reporter, datetime.datetime.now(), category, news_body, images, url)
        else:
            print("Failed to scrape the news data.")
