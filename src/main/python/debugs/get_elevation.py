import requests
import urllib
import urllib3
import pandas as pd

url = r'https://nationalmap.gov/epqs/pqs.php?'


# coordinates with known elevation (905m)
# lat = [-21.243481 ]
# lon = [-45.004072 ],
def make_remote_request(url: str, params: dict):
    """
    Makes the remote request
    Continues making attempts until it succeeds
    """

    count = 1
    while True:
        try:
            response = requests.get((url + urllib.parse.urlencode(params)))
        except (OSError, urllib3.exceptions.ProtocolError) as error:
            print('\n')
            print('*' * 20, 'Error Occured', '*' * 20)
            print(f'Number of tries: {count}')
            print(f'URL: {url}')
            print(error)
            print('\n')
            count += 1
            continue
        break

    return response


def eleveation_function(x):
    url = 'https://nationalmap.gov/epqs/pqs.php?'
    params = {'x': x[1],
              'y': x[0],
              'units': 'Meters',
              'output': 'json'}
    result = make_remote_request(url, params)
    return result.json()['USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation']


# coordinates with known elevation
lat = [48.633, 48.733, 45.1947, 45.1962, -21.243481]
lon = [-93.9667, -94.6167, -93.3257, -93.2755, -45.004072]

# create df
df = pd.DataFrame({'lat': lat, 'lon': lon})

# apply the function
df['elevations'] = df.apply(eleveation_function, axis=1)

print(df)
