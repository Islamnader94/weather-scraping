import requests
import pandas as pd
from sqlalchemy import create_engine
from bs4 import BeautifulSoup

#SQL connection data to connect and save the data in
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="scraping_user",
                               pw="1234",
                               db="scraping_sample"))


urls = ['https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.XgClahczbRY',
        'https://freemeteo.ae/weather/dubai/7-days/list/?gid=292223&language=english&country=united-arab-emirates' ]

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # import pudb;
    # pudb.set_trace();
    if url == urls[0]:
        forcast_weathers = soup.find(id='seven-day-forecast-body')
        forcast_weathers_data = forcast_weathers.find_all(class_='forecast-tombstone')
        period = [forcast.find(class_='period-name').get_text() for forcast in forcast_weathers_data]
        short_desc = [forcast.find(class_='short-desc').get_text() for forcast in forcast_weathers_data]
        tempreture = [forcast.find(class_='temp').get_text() for forcast in forcast_weathers_data]
        weather = pd.DataFrame({
            'country': 'San Francisco',
            'period': period,
            'discription': short_desc,
            'tempreture': tempreture
        })
        try:
            # Execute the SQL command
            weather.to_sql('weather', con = engine, if_exists = 'append', chunksize = 1000, index=False)
            print('Appending finished!')
            print('==================')
        except:
            print('Failed to Append')
    elif url == urls[1]:
        # print(soup.prettify())
        weather_network = soup.find(class_='today')
        weather_network_data = weather_network.find_all(class_='day')
        period = [weather.find('b').get_text() for weather in weather_network_data]
        short_desc = [weather.find(class_='info').get_text() for weather in weather_network_data]
        tempreture = [weather.find(class_='temps').get_text() for weather in weather_network_data]

        dubai_weather = pd.DataFrame({
            'country': 'Dubai',
            'period': period,
            'discription': short_desc,
            'tempreture': tempreture
        })
        try:
            # Execute the SQL command
            dubai_weather.to_sql('weather', con = engine, if_exists = 'append', chunksize = 1000, index=False)
            print('Appending finished!')
        except:
            print('Failed to Append')
