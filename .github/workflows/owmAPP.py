import owm from pyowm


API_key = '2453e6f83f6da666090dbc7ba0182843'
owm = OWM(API_key, language='de')

obs = owm.weather_at_place('Kelkheim,DE')

# time = obs.get_reception_time(timeformat='iso')           # ISO8601

w = obs.get_weather()

time = w.get_reference_time(timeformat='iso')
w.get_reference_time()
w.get_clouds()


print (time)