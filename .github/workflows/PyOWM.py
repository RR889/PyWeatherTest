'''
SETUP:

Documentation:
https://pyowm.readthedocs.io/en/latest/

API-Key:
2453e6f83f6da666090dbc7ba0182843

https://github.com/csparpa/pyowm

Soil Data:
https://pyowm.readthedocs.io/en/latest/usage-examples-v2/agro-api-usage-examples.html


'''
import csv
import pyowm

API_key = '2453e6f83f6da666090dbc7ba0182843'
owm = pyowm.OWM(API_key, language='de')


# Search for current weather in London (Great Britain)
# obs = owm.weather_at_id(2643741)                           # City ID
# obs = owm.weather_at_coords(-0.107331,51.503614)           # lat/lon
obs = owm.weather_at_place('Kelkheim,DE')


w = obs.get_weather()


# Weather details
time = w.get_reference_time(timeformat='iso')

humd = w.get_humidity()              # 87
temp = w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

clouds = w.get_clouds()                                     # Get cloud coverage
rain = w.get_rain()                                       # Get rain volume
snow = w.get_snow()                                       # Get snow volume
wind = w.get_wind()                                       # Get wind degree and speed {'deg': 59, 'speed': 2.660}
press = w.get_pressure()                                   # Get atmospheric pressure {'press': 1009, 'sea_level': 1038.381}

st = w.get_status()                                     # Get weather short status
stDet = w.get_detailed_status()                           # Get detailed weather status 'Broken clouds'

code  = w.get_weather_code()                               # Get OWM weather condition code
icon =  w.get_weather_icon_name()                          # Get weather-related icon name'02d'
iconURL = w.get_weather_icon_url()                          # Get weather-related icon URL 'http://openweathermap.org/img/w/02d.png'

sun_r = w.get_sunrise_time('iso')                          # Sunrise time (GMT UNIXtime or ISO 8601)1377862896L
sun_s = w.get_sunset_time('iso')                           # Sunset time (GMT UNIXtime or ISO 8601)

#print(time, temp, humd, wind, st, stDet, clouds, rain, press, code, sun_r,sun_s; )
print('\nZeit: ', time)
print('Sunrise: ', sun_r)
print('Sunset: ', sun_s)

print('\nStatus: ', stDet)

print('\nTemperatur: ', temp)
print('RLF: ', humd, '%')
print('Clouds: ', clouds)
print('Icon: ', icon)
print('Icon-URL: ', iconURL)


# Search current weather observations in the surroundings of
# lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
# observation_list = owm.weather_around_coords(-22.57, -43.12)


'''
file = open('weatherDataLog.txt', 'w');
file.write(data.to_string());    // if data is a pandas.DataFrame object
file.close();

To do:
How to print on dashboard
for loop
save data
'''

with open ('mycsv.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['col1', 'col2', 'col3'])            # col1, col2, col3
    #thewriter.writerow(['col1', 'col2', 'col3'])

    #for i in range(1, 100):
    #csv_writer.writerow(['one', 'two', 'three'])             # one, two, three    (100x, da for Schleife)


# csv module’s reader and writer objects --> read and write sequences
# DictReader and DictWriter classes --> read and write data in dictionary form



#    https: // www.youtube.com / watch?v = s1XiCh - mGCA
