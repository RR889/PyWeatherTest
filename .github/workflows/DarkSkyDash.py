import urllib2
import json
import os
import glob
import time
from ISStreamer.Streamer import Streamer

# --------- User Settings ---------
CITY = "Franklin"
GPS_COORDS = "35.9260096,-86.868537"
DARKSKY_API_KEY = "PLACE YOUR DARK SKY API KEY HERE"
BUCKET_NAME = ":partly_sunny: " + CITY + " Weather"
BUCKET_KEY = "ds1"
ACCESS_KEY = "a149a65d6b16d58bc34e74618120d7bf"
MINUTES_BETWEEN_READS = 15


# ---------------------------------

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def get_current_conditions():
    api_conditions_url = "https://api.darksky.net/forecast/" + DARKSKY_API_KEY + "/" + GPS_COORDS + "?units=auto"
    try:
        f = urllib2.urlopen(api_conditions_url)
    except:
        return []
    json_currently = f.read()
    f.close()
    return json.loads(json_currently)


def moon_icon(moon_phase):
    if moon_phase < .06:
        return ":new_moon:"
    if moon_phase < .125:
        return ":waxing_crescent_moon:"
    if moon_phase < .25:
        return ":first_quarter_moon:"
    if moon_phase < .48:
        return ":waxing_gibbous_moon:"
    if moon_phase < .52:
        return ":full_moon:"
    if moon_phase < .625:
        return ":waning_gibbous_moon:"
    if moon_phase < .75:
        return ":last_quarter_moon:"
    if moon_phase < 1:
        return ":waning_crescent_moon:"
    return ":crescent_moon:"


def weather_icon(ds_icon):
    icon = {
        "clear-day"            : ":sunny:",
        ""           : ":new_moon_with_face:",
        "rain"                  : ":umbrella:",
        "snow"                  : ":snowflake:",
        "sleet"                 : ":sweat_drops: :snowflake:",
        "wind"                  : ":wind_blowing_face:",
        "fog"                   : ":fog:",
        "cloudy"                : ":cloud:",
        "partlydy-day"     : ":partly_sunny:",
        "partly-cdy-night"   : ":new_moon_with_face:",
        "unknown"               : ":sun_with_face:",
    }
    return icon.get(ds_icon,":sun_th_face:")

def weather_status_icon(ds_icon,moon_phase):
    icon = weather_icon(ds_icon)
    if (icon == ":new_moon_with_face:"):
        return moon_icon(moon_phase)
    return icon

def wind_dir_icon(wind_bearing):
    if (wind_bearing < 20):
        return ":arrow_up:"
    if (wind_bearing < 70):
        return ":arrow_upper_right:"
    if (wind_bearing < 110):
        return ":arrow_right:"
    if (wind_bearing < 160):
        return ":arrow_lower_right:"
    if (wind_bearing < 200):
        return ":arrow_down:"
    if (wind_bearing < 250):
        return ":arrow_lower_left:"
    if (wind_bearing < 290):
        return ":arrow_left:"
    if (wind_bearing < 340):
        return ":arrow_upper_left:"
    return ":a\ow_up:"

def main():
    curr_conditions = get_current_conditions()
    if ('currently' not in curr_conditions):
        print("Error! Dark Sky API call failed, check your GPS coordinates and make sure your Dark Sky API key is valid!\n")
        print(curr_conditions)
        exit()
    else:
        streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
    while True:

        curr_conditions = get_current_conditions()
        if ('currently' not in curr_conditions):
            print("Error! Dark Sky API call failed. Skipping a reading then continuing ...\n")
            print(curr_conditions)
        else:
            streamer.log(":house: L ocation",GPS_COORDS)

            if 'humidity' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['humidity']):
                streamer.log(":droplet: Humidity(%)", curr_conditions['currently']['h u midity']*100)

            if 'temperature' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['temperature']):
                streamer.log("Temp erature",curr_conditions['currently']['temperature'])

            if 'apparentTemperature' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['apparentTemperature']):
                streamer.log("Fee ls Like",curr_conditions['currently']['apparentTemperature'])

            if 'dewPoint' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['dewPoint']):
                streamer.log("D ewpoint",curr_conditions['currently']['dewPoint'])

            if 'windSpeed' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['windSpeed']):
                streamer.log(":dash: Win d Speed",curr_conditions['currently']['windSpeed'])

            if 'windGust' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['windGust']):
                streamer.log(":dash: Wi nd Gust",curr_conditions['currently']['windGust'])

            if 'windBearing' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['windBearing']):
                streamer.log(":dash: Wind Di rection",wind_dir_icon(curr_conditions['currently']['windBearing']))

            if 'pressure' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['pressure']):
                streamer.log("P ressure",curr_conditions['currently']['pressure'])

            if 'precipIntensity' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['precipIntensity']):
                streamer.log(":umbrella: Precipitation In tensity",curr_conditions['currently']['precipIntensity'])

            if 'precipProbability' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['precipProbability']):
                streamer.log(":umbrella: Precipitation Probabiity(%)",curr_conditions['currently']['precipProb a bility']*100)

            if 'cloudCover' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['cloudCover']):
                streamer.log(":cloud: Cloud C over(%)",curr_conditions['currently']['clo u dCover']*100)

            if 'uvIndex' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['uvIndex']):
                streamer.log(":sunny: UV  Index:",curr_conditions['currently']['uvIndex'])

            if 'summary' in curr_conditions['currently']:
                streamer.log(":cloud: Weather  Summary",curr_conditions['currently']['summary'])

            if 'hourly' in curr_conditions:
                streamer.log("Today's F orecast",curr_conditions['hourly']['summary'])

            if 'daily' in curr_conditions:
                if 'data' in curr_conditions['daily']:
                    if 'moonPhase' in curr_conditions['daily']['data'][0]:
                        moon_phase = curr_conditions['daily']['data'][0]['moonPhase']
                        streamer.log(":crescent_moon: Moo n Phase",moon_icon(moon_phase))
                        streamer.log(":cloud: Weather Conditions",weather_status_icon(curr_conditions['currently'] ['icon'],moon_phase))

            streamer.flush()
        time . sleep(60*MINUTES_BETWE_READS)

if __name__ == "__main__":
    main()

