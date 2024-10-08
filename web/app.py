from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper
import requests
import sys
import os

app = Flask(__name__)

weather_api_key = os.environ['OPEN_WEATHER_API_KEY']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        city_name = request.form['city_name']
        return redirect(url_for('add_city', city=city_name))
    return render_template('index.html')


@app.route('/profile')
def profile():
    return 'This is the profile page'


@app.route('/login')
def log_in():
    return 'This is login page'


weather_list = []
@app.route('/add/<city>', methods=['GET', 'POST'])
def add_city(city):
    if request.method == "GET":
        #city_name = request.form['city_name']
        weather_data = get_weather_data(city)
        if weather_data:
            weather_list.append(weather_data)
        return render_template('index.html', weather=weather_list)


def get_weather_data(city_name):

    long_lat = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={weather_api_key}').json()
    if long_lat:
        print(long_lat)
        long = long_lat[0]['lon']
        lat = long_lat[0]['lat']
    else:
        return 'Error encountered in getting Long and Lat'

    weather_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={long}&units=metric&appid={weather_api_key}'
    weather_data = requests.get(weather_url).json()
    if weather_data:
        print(weather_data)
        state = weather_data['current']['weather'][0]['main']
        degrees = weather_data['current']['temp']
        city = city_name

        return {'degrees': degrees,
                'state': state,
                'city': city}


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
